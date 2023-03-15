import definitions
from typing import NamedTuple

JSON_FB = 'fb_json'
JSON_HEAD = 'head'
JSON_VALUE = 'value'

# prefix used to create json object handler
JSON_PREFIX = 'json_'

def add_objectStart(item, json_parent):
    # IF    fb_json.HasMember(jsonDoc, 'recipeList')     THEN
    # json_recipeList := fb_json.FindMember(jsonDoc, 'recipeList');
    prefixed_p = JSON_PREFIX + json_parent
    res = ''
    res = res + 'IF ' + JSON_FB + '.HasMember(' + prefixed_p + ', \'' + item.name + '\') THEN\n'
    res = res + JSON_PREFIX + item.name + ' := ' + JSON_FB + '.FindMember(' + prefixed_p + ', \'' + item.name + '\');\n'
    return res


def add_objectEnd(item, json_parent):
    res = ''
    res = res + 'END_IF\n'
    return res


def add_arrayStart(item, json_parent, array_level):
    # IF fb_json.IsArray(json_recipeList) THEN
    #    FOR i := 0 TO MIN(TO_INT(fb_json.GetArraySize(json_recipeList)), CONST.MAX_RECIPE_NUMBER - start_at+1) BY 1 DO
    #        json_i := fb_json.GetArrayValueByIdx(json_recipeList, i);
    prefixed_p = JSON_PREFIX + json_parent
    res = ''
    res = res + 'IF ' + JSON_FB + '.IsArray(' + prefixed_p + ') THEN \n'
    res = res + 'FOR ' + 'i' * array_level + ' := 0 TO MIN(TO_INT(' + JSON_FB + '.GetArraySize(' + prefixed_p + ')) - 1, ' + item.stop_at + ' - ' + item.start_at + ') BY 1 DO\n'
    res = res + JSON_PREFIX + 'i' * array_level + ' := ' + JSON_FB + '.GetArrayValueByIdx(' + prefixed_p + ', TO_UDINT(' + 'i' * array_level + '));\n'
    return res


def add_arrayEnd(item):
    res = ''
    res = res + 'END_FOR\n'
    res = res + 'END_IF\n'
    return res


def add_valueItem(namespace, item, json_parent, array_level):
    # IF fb_json.HasMember(json_ST110_02Z, 'rVeloToIn') THEN
    #     jsonValue := fb_json.FindMember(json_ST110_02Z, 'rVeloToIn');
    #     PERS.recipeList[i].st110.ST110_02Z.rVeloToIn := TO_REAL(fb_json.GetDouble(jsonValue));
    # END_IF

    try:
        prefixed_p = JSON_PREFIX + json_parent
        prefixed_v = JSON_PREFIX + JSON_VALUE
        var_name = item.name
        if array_level > 0:
            var_name = var_name + '[' + 'i' * array_level + ' + ' + item.start_at + ']'
            prefixed_v = JSON_PREFIX + json_parent


        res = ''
        if 0 == array_level:
            res = res + 'IF ' + JSON_FB + '.HasMember(' + prefixed_p + ', \'' + item.name + '\') THEN \n'
            res = res + prefixed_v + ' := ' + JSON_FB + '.FindMember(' + prefixed_p + ', \'' + item.name + '\');\n'

        if item.var_type in definitions.keywords_int:
            res = res + namespace + var_name + ' := TO_' + item.var_type + '(' + JSON_FB + '.GetInt(' + prefixed_v + '));\n'

        elif item.var_type in definitions.keywords_string:
            res = res + namespace + var_name + ' := ' + JSON_FB + '.GetString(' + prefixed_v + ');\n'

        elif item.var_type in definitions.keywords_float:
            res = res + namespace + var_name + ' := TO_' + item.var_type + '(' + JSON_FB + '.GetDouble(' + prefixed_v + '));\n'

        elif item.var_type in definitions.keywords_bool:
            res = res + namespace + var_name + ' := TO_' + item.var_type + '(' + JSON_FB + '.GetBool(' + prefixed_v + '));\n'

        res = res + 'END_IF\n'
        return res

    except AttributeError:
        return ''


def get_local_var_str(var_list, i_level):

    res = JSON_FB + ' : FB_JsonDomParser;\n\n'

    for x in var_list:
        res = res + JSON_PREFIX + x + ': SJsonValue;\n'

    for i in range(1, i_level+1):
        res = res + JSON_PREFIX + 'i'*i + ' : SJsonValue;\n'

    for i in range(1, i_level+1):
        res = res + '\n' + 'i'*i + ' : INT;\n'

    return res


def parse_reader(object_list, start_namespace):
    array_level = 0
    namespace: str = start_namespace

    parents = [JSON_HEAD]
    variables = [JSON_HEAD, JSON_VALUE]
    res = JSON_PREFIX + JSON_HEAD + ' := ' + JSON_FB + '.ParseDocument(sMessage);\n\n'

    max_array_level = 0

    for item in object_list:
        if isinstance(item, definitions.ArrayVariable):
            res = res + add_objectStart(item, parents[-1])
            parents.append(item.name)
            variables.append(item.name)
            array_level = array_level + 1
            res = res + add_arrayStart(item, parents[-1], array_level)
            array_iterable = 'i'*array_level
            parents.append(array_iterable)
            res = res + add_valueItem(namespace, item, parents[-1], array_level)
            res = res + add_arrayEnd(item)
            res = res + add_objectEnd(item, parents[-1])
            array_level = array_level - 1
            parents.pop()
            parents.pop()

        elif isinstance(item, definitions.SimpleVariable):
            res = res + add_valueItem(namespace, item, parents[-1], 0)
            
        elif isinstance(item, definitions.Enum):
             res = res + add_valueItem(namespace, item, parents[-1], 0)

        elif isinstance(item, definitions.ObjectVariableStart):
            res = res + add_objectStart(item, parents[-1])
            namespace = namespace + item.name + '.'
            parents.append(item.name)
            variables.append(item.name)

        elif isinstance(item, definitions.ObjectVariableEnd):
            res = res + add_objectEnd(item, parents[-1])
            namespace = namespace.rsplit('.', 2)[0] + '.'
            parents.pop()

        elif isinstance(item, definitions.ArrayVariableStart):
            array_level = array_level + 1
            namespace = namespace + item.name + '[' + 'i' * array_level + ' + ' + item.start_at + '].'
            res = res + add_objectStart(item, parents[-1])
            parents.append(item.name)
            variables.append(item.name)
            res = res + add_arrayStart(item, parents[-1], array_level)
            array_iterable = 'i'*array_level
            parents.append(array_iterable)

        elif isinstance(item, definitions.ArrayVariableEnd):
            array_level = array_level - 1
            namespace = namespace.rsplit('.', 2)[0] + '.'
            res = res + add_arrayEnd(item)
            res = res + add_objectEnd(item, parents[-1])
            parents.pop()
            parents.pop()

        max_array_level = max(max_array_level, array_level)

    return res, get_local_var_str(variables, max_array_level)

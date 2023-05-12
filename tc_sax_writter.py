import definitions

JSON_VAR = 'refJsonWriter'

header = '{json_var}.ResetDocument();\n' \
         '// global object\n' \
         '{json_var}.StartObject();\n\n'.format(json_var=JSON_VAR)

footer = '\n// end global object\n' \
         '{json_var}.EndObject();\n'.format(json_var=JSON_VAR)


def add_startArray(start, end, i_level):
    res = JSON_VAR + '.StartArray();\n'
    res = res + 'FOR ' + 'i' * i_level + ' := ' + start + ' TO ' + end + ' BY 1 DO\n'
    return res


def add_endArray():
    res = 'END_FOR\n'
    res = res + JSON_VAR + '.EndArray();\n'
    return res


def add_BasicType(namespace, item, str_array):
    if item.var_type in definitions.keywords_int:
        if item.var_type == 'DWORD':
            return JSON_VAR + '.AddUdint(' + namespace + item.name + str_array + ');\n'
        elif item.var_type == 'ULINT':
            return JSON_VAR + '.AddUlint(' + namespace + item.name + str_array + ');\n'
        elif item.var_type == 'LWORD':
            return JSON_VAR + '.AddUlint(' + namespace + item.name + str_array + ');\n'
        elif item.var_type == 'LINT':
            return JSON_VAR + '.AddLint(' + namespace + item.name + str_array + ');\n'
        elif item.var_type == 'DWORD':
            return JSON_VAR + '.AddUdint(' + namespace + item.name + str_array + ');\n'
        elif item.var_type == 'UDINT':
            return JSON_VAR + '.AddUdint(' + namespace + item.name + str_array + ');\n'
        else:
            return JSON_VAR + '.AddDint(' + namespace + item.name + str_array + ');\n'

    elif item.var_type in definitions.keywords_string:
        return JSON_VAR + '.AddString(\'' + namespace + item.name + str_array + '\');\n'

    elif item.var_type in definitions.keywords_float:
        return JSON_VAR + '.AddLreal(' + namespace + item.name + str_array + ');\n'

    elif item.var_type in definitions.keywords_bool:
        return JSON_VAR + '.AddBool(' + namespace + item.name + str_array + ');\n'

    elif item.var_type in definitions.keywords_time_res_ms:
        return JSON_VAR + '.AddDint(TIME_TO_DINT(' + namespace + item.name + str_array + '));\n'

    else:
        print('type <{type}> not found during writer creation'.format(type=item.var_type))
        return ''


def add_enum(namespace, item: definitions.Enum):
    res = JSON_VAR + '.AddKey(\'' + item.name + '\');\n'
    res = res + add_BasicType(namespace, item, '')
    return res


def add_SimpleVariable(namespace, item: definitions.SimpleVariable):
    res = JSON_VAR + '.AddKey(\'' + item.name + '\');\n'
    res = res + add_BasicType(namespace, item, '')
    return res


def add_ArrayVariable(namespace, item: definitions.ArrayVariable, i_level):
    res = JSON_VAR + '.AddKey(\'' + item.name + '\');\n'
    res = res + add_startArray(item.start_at, item.stop_at, i_level)

    res = res + add_BasicType(namespace, item, '[' + 'i' * i_level + ']')

    res = res + add_endArray()
    return res


def add_ObjectVariableStart(namespace, item: definitions.ObjectVariableStart):
    res = JSON_VAR + '.addKey(\'' + item.name + '\');\n'
    res = res + JSON_VAR + '.StartObject();\n'
    return res


def add_ObjectVariableEnd(namespace, item: definitions.ObjectVariableEnd):
    return JSON_VAR + '.EndObject();\n'


def add_ArrayVariableStart(namespace, item: definitions.ArrayVariableStart, i_level):
    res = JSON_VAR + '.addKey(\'' + item.name + '\');\n'
    res = res + add_startArray(item.start_at, item.stop_at, i_level)
    res = res + JSON_VAR + '.StartObject();\n'
    return res


def add_ArrayVariableEnd(namespace, item: definitions.ArrayVariableEnd):
    res = JSON_VAR + '.EndObject();\n'
    res = res + add_endArray()
    return res


def get_local_var_str(i_level):
    res = 'refJsonWriter : REFERENCE TO FB_JsonSaxWriter;\n\n'
    for i in range(1, i_level + 1):
        res = res + 'i' * i + ' : INT;\n'

    return res


def parse_writer(object_list, start_namespace):
    write_fb_string = ''
    indent_level = 0
    namespace = start_namespace
    write_fb_string = write_fb_string + header
    max_indent_level = 0

    for item in object_list:
        if isinstance(item, definitions.ArrayVariable):
            write_fb_string = write_fb_string + add_ArrayVariable(namespace, item, indent_level + 1)

        elif isinstance(item, definitions.SimpleVariable):
            write_fb_string = write_fb_string + add_SimpleVariable(namespace, item)

        elif isinstance(item, definitions.ObjectVariableStart):
            write_fb_string = write_fb_string + add_ObjectVariableStart(namespace, item)
            namespace = namespace + item.name + '.'

        elif isinstance(item, definitions.ObjectVariableEnd):
            write_fb_string = write_fb_string + add_ObjectVariableEnd(namespace, item)
            namespace = namespace.rsplit('.', 2)[0] + '.'

        elif isinstance(item, definitions.ArrayVariableStart):
            indent_level = indent_level + 1
            write_fb_string = write_fb_string + add_ArrayVariableStart(namespace, item, indent_level)
            namespace = namespace + item.name + '[' + 'i' * indent_level + '].'

        elif isinstance(item, definitions.ArrayVariableEnd):
            indent_level = indent_level - 1
            write_fb_string = write_fb_string + add_ArrayVariableEnd(namespace, item)
            namespace = namespace.rsplit('.', 2)[0] + '.'

        elif isinstance(item, definitions.Enum):
            write_fb_string = write_fb_string + add_enum(namespace, item)

        max_indent_level = max(max_indent_level, indent_level)

    write_fb_string = write_fb_string + footer

    print(max_indent_level)
    return write_fb_string, get_local_var_str(max_indent_level)

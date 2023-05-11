import definitions

header = 'fbJson.ResetDocument();\n' \
         '//  global object\n' \
         'fbJson.StartObject();\n\n'

footer = '\n\n// end global object\n' \
         'fbJson.EndObject();\n' \
         '// end of file\n' \
         'SaveInMemory_Recipe := TO_DINT(fbJson.CopyDocument(sData, fbJson.GetDocumentLength()));\n' \
         'fbJson.ResetDocument();\n'


def add_startArray(start, end, i_level):
    res = ('fbJson.StartArray();\n')
    res = res + 'FOR ' + 'i' * i_level + ' := ' + start + ' TO ' + end + ' BY 1 DO\n'
    return res


def add_endArray():
    res = 'END_FOR\n'
    res = res + 'fbJson.EndArray();\n'
    return res


def add_BasicType(namespace, item, str_array):
    if item.var_type in definitions.keywords_int:
        if item.var_type == 'DWORD':
            return 'fbJson.AddUdint(' + namespace + item.name + str_array + ');\n'
        elif item.var_type == 'ULINT':
            return 'fbJson.AddUlint(' + namespace + item.name + str_array + ');\n'
        elif item.var_type == 'LWORD':
            return 'fbJson.AddUlint(' + namespace + item.name + str_array + ');\n'
        elif item.var_type == 'LINT':
            return 'fbJson.AddLint(' + namespace + item.name + str_array + ');\n'
        elif item.var_type == 'DWORD':
            return 'fbJson.AddUdint(' + namespace + item.name + str_array + ');\n'
        elif item.var_type == 'UDINT':
            return 'fbJson.AddUdint(' + namespace + item.name + str_array + ');\n'
        else:
            return 'fbJson.AddDint(' + namespace + item.name + str_array + ');\n'

    elif item.var_type in definitions.keywords_string:
        return 'fbJson.AddString(\'' + namespace + item.name + str_array + '\');\n'

    elif item.var_type in definitions.keywords_float:
        return 'fbJson.AddLreal(' + namespace + item.name + str_array + ');\n'

    elif item.var_type in definitions.keywords_bool:
        return 'fbJson.AddBool(' + namespace + item.name + str_array + ');\n'

    elif item.var_type in definitions.keywords_time_res_ms:
        return 'fbJson.AddDint(TIME_TO_DINT(' + namespace + item.name + str_array + '));\n'

    else:
        print('type <{type}> not found during writter creation'.format(type=item.var_type))
        return ''


def add_enum(namespace, item: definitions.Enum):
    res = 'fbJson.AddKey(\'' + item.name + '\');\n'
    res = res + add_BasicType(namespace, item, '')
    return res

def add_SimpleVariable(namespace, item: definitions.SimpleVariable):
    res = 'fbJson.AddKey(\'' + item.name + '\');\n'
    res = res + add_BasicType(namespace, item, '')
    return res


def add_ArrayVariable(namespace, item: definitions.ArrayVariable, i_level):
    res = 'fbJson.AddKey(\'' + item.name + '\');\n'
    res = res + add_startArray(item.start_at, item.stop_at, i_level)

    res = res + add_BasicType(namespace, item, '[' + 'i' * i_level + ']')

    res = res + add_endArray()
    return res


def add_ObjectVariableStart(namespace, item: definitions.ObjectVariableStart):
    res = 'fbJson.addKey(\'' + item.name + '\');\n'
    res = res + 'fbJson.StartObject();\n'
    return res


def add_ObjectVariableEnd(namespace, item: definitions.ObjectVariableEnd):
    return 'fbJson.EndObject();\n'


def add_ArrayVariableStart(namespace, item: definitions.ArrayVariableStart, i_level):
    res = 'fbJson.addKey(\'' + item.name + '\');\n'
    res = res + add_startArray(item.start_at, item.stop_at, i_level)
    res = res + 'fbJson.StartObject();\n'
    return res


def add_ArrayVariableEnd(namespace, item: definitions.ArrayVariableEnd):
    res = 'fbJson.EndObject();\n'
    res = res + add_endArray()
    return res


def get_local_var_str(i_level):
    res = 'fbJson : FB_JsonSaxWriter;\n\n'
    for i in range(1, i_level+1):
        res = res + 'i'*i + ' : INT;\n'

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
    
    print (max_indent_level)
    return write_fb_string, get_local_var_str(max_indent_level)

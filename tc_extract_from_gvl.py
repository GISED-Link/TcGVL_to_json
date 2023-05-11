import os
import re
import definitions


def extract_from_string(text_to_search, search_for_json, namespace):
    token_specification = [
        ('VARIABLE', definitions.find_var),
        ('ARRAY', definitions.find_var_array),
        ('TO_JSON', definitions.find_to_json_attribute),
        ('EXTENDED', definitions.find_extends)
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    flag_to_json = False
    for mo in re.finditer(tok_regex, text_to_search):
        kind = mo.lastgroup
        index = mo.lastindex
        if kind == 'VARIABLE':
            if flag_to_json or not search_for_json:
                print(f'VARIABLE type found with name {mo.groups()[index]} and type {mo.groups()[index + 2]}')
                yield definitions.SimpleVariable(namespace, mo.groups()[index], mo.groups()[index + 1],
                                                 mo.groups()[index + 2])
        elif kind == 'ARRAY':
            if flag_to_json or not search_for_json:
                print(f'ARRAY type found with name {mo.groups()[index]}')
                yield definitions.ArrayVariable(namespace, mo.groups()[index], mo.groups()[index + 1],
                                        mo.groups()[index + 2], mo.groups()[index + 3], mo.groups()[index + 4])

        elif kind == 'EXTENDED' and not search_for_json:
            print(f'Extended type found with name {mo.groups()[index]}')
            namespace_split, var_name, *garbage = namespace.rsplit('.', 2)
            yield definitions.ExtendedVariable(namespace_split + '.', var_name, mo.groups()[index])
        
        if kind == 'TO_JSON':
            flag_to_json = True
        elif flag_to_json:
            flag_to_json = False

def search_file(path, type_name):
    name_to_search = type_name + '.TcDUT'
    for root, d_names, f_names in os.walk(path):
        if name_to_search in f_names:
            return name_to_search
        else:
            for directory in d_names:
                file_name_tmp = search_file(path + '/' + str(directory), type_name)
                if file_name_tmp is not None:
                    return str(directory) + '/' + file_name_tmp

def add_end_object(object_local, var_list):
    if isinstance(object_local, definitions.ArrayVariable):
        var_list.append(definitions.ArrayVariableEnd())
    else:
        var_list.append(definitions.ObjectVariableEnd())

def add_start_object(object_local, var_list):
    if isinstance(object_local, definitions.ArrayVariable):
        var_list.append(
            definitions.ArrayVariableStart(object_local.namespace, object_local.name, object_local.start_at,
                                           object_local.stop_at))

    else:
        var_list.append(
            definitions.ObjectVariableStart(object_local.namespace, object_local.name, object_local.var_type))

def check_if_type_known_from_token(token_local, var_list, searched_path):
    flag_type_known = False
    for sublist in definitions.keywords_supported:
        
        if token_local.var_type in sublist:
            flag_type_known = True
            var_list.append(token_local)
            break
    if not flag_type_known:
        print('search type ' + token_local.var_type)
        file_name = search_file(searched_path, token_local.var_type)
        if file_name is not None:    
            if isinstance(token_local, definitions.ExtendedVariable):
                print(f'file name of extended file is {file_name}')
                print(f'namespace is {token_local.namespace}')
                print(f'end_name is {token_local.end_name}')  
                get_token_from_files(file_name, token_local.namespace + token_local.end_name + '.', var_list, searched_path)
            else:
                checkEnum,typeEnum=check_isEnum(file_name,searched_path)
                if(checkEnum):
                    enum=definitions.Enum(token_local.namespace,token_local.name,token_local.address,typeEnum)
                    var_list.append(enum)
                else:
                    add_start_object(token_local, var_list)
                    get_token_from_files(file_name, token_local.namespace + token_local.name + '.', var_list, searched_path)
                    add_end_object(token_local, var_list)
        else:
            print('file not found')

def get_token_from_files(type_file_name, namespace, variable_to_parse, search_path):
    file_to_extract = [type_file_name]
    extract_index = 0
    try:
        while extract_index < 100:
            my_file_local = open(search_path + file_to_extract[extract_index], mode='rt')
            extract_index = extract_index + 1
            text_local = my_file_local.read()
            my_file_local.close()
            for token_r in extract_from_string(text_local, False, namespace):
                check_if_type_known_from_token(token_r, variable_to_parse, search_path)

    # Since we append periodically, we search until the end
    except IndexError:
        print(f'{type_file_name.rsplit("/", 1)[1]} extraction complete. {extract_index} type has been extracted')
        pass


def extract_token_from_file(tcgvl_file_name, search_path):
    ''' extract all {attribute \'to_json\'} '''
    variable_to_parse = []
    my_file = open(tcgvl_file_name, mode='rt')
    text = my_file.read()

    my_file.close()
    namespace = my_file.name.rsplit('.', 1)[0]
    namespace = namespace.rsplit('/', 1)[1]
    for token in extract_from_string(text, True, namespace + '.'):
        check_if_type_known_from_token(token, variable_to_parse, search_path)
        

    return variable_to_parse, namespace

def check_isEnum(type_file_name, search_path):
    typeEnum=""
    file_to_extract = [type_file_name]
    extract_index = 0
    my_file_local = open(search_path + file_to_extract[extract_index], mode='rt')
    extract_index = extract_index + 1
    text_local = my_file_local.read()
    my_file_local.close()
    find=re.findall(definitions.find_enum,text_local)
    
    if(find!=[]):
        typeEnum=find[0][1]
        result=True
    else: result=False
    return result,typeEnum

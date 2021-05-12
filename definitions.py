from typing import NamedTuple

keywords_int = ['BYTE', 'WORD', 'DWORD', 'LWORD', 'SINT', 'USINT', 'INT', 'UINT', 'DINT', 'UDINT', 'LINT', 'ULINT']
keywords_bool = ['BOOL']
keywords_float = ['REAL', 'LREAL']
keywords_string = ['STRING', 'WSTRING']
keywords_time = ['TIME', 'TIME_OF_DAY', 'DATE', 'DATE_AND_TIME', 'LTIME']
keywords_array = ['ARRAY']
keywords_unsupported = ['ANY', 'ANY_BIT', 'ANY_DATE', 'ANY_NUM', 'ANY_REAL', 'ANY_INT', 'ANY_STRING', 'XINT', 'UXINT',
                        'XWORD', 'PVOID', 'POINTER', 'REFERENCE']
keywords_union = ['UNION']
keywords_struct = ['STRUCT']
keywords_enum = ['ENUM']

keywords_supported = [keywords_int, keywords_bool, keywords_float, keywords_string]

find_type = r'.*:[ \t]*([A-z]+).*;.*$'
find_comment = r'^.*[\/]*'
find_to_json_attribute = r'[ \t]*{[ \t]*attribute[ \t]*\'to_json\'[ \t]*}.*\n'
find_var = r'[ \t]*([A-z0-9]*)[ \t\n]+(AT%[A-z0-9*]*)?[ \t\n]*:[ \t\n]*([A-z0-9]*)[ \t\n]*(:=)?[ \t\n]*[A-z0-9]*[ \t\n]*;'
find_var_array = r'[ \t]*([A-z0-9]+)[ \t\n]+(AT%[A-z\d*]+)?[ \t\n]*:[ \t\n]*ARRAY[ \t\n]*.[ \t\n]*([A-z\d]+)[ \t\n]*\.\.[ \t\n]*([A-z\d\.]+)[ \t\n]*.[ \t\n]+OF[ \t\n]+([A-z\d]+);'
find_to_json_attribute = r'\n[ \t]*\{[ \t]*attribute[ \t]+\'to_json\'[ \t]*\}[ \t]*\n'


class ArrayVariable(NamedTuple):
    namespace: str
    name: str
    address: str
    start_at: str
    stop_at: str
    var_type: str


class SimpleVariable(NamedTuple):
    namespace: str
    name: str
    address: str
    var_type: str


class ObjectVariableStart(NamedTuple):
    namespace: str
    name: str
    var_type: str


class ObjectVariableEnd(NamedTuple):
    pass  # this class is left empty


class ArrayVariableStart(NamedTuple):
    namespace: str
    name: str
    start_at: str
    stop_at: str


class ArrayVariableEnd(NamedTuple):
    pass  # this class is left empty

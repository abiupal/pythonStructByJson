
from struct import *

def getStructFormat(endian, datatype, bytesize):
    target_format = endian
    format = ''
    format_size = bytesize
    if "char" == datatype:
        format = 'c'
    elif "unsigned char" == datatype:
        format = 'B'
    elif "short" == datatype:
        format = 'h'
        format_size = format_size / 2
    elif "unsigned short" == datatype:
        format = 'H'
        format_size = format_size / 2
    elif "long" == datatype:
        format = 'l'
        format_size = format_size / 4
    elif "unsigned long" == datatype:
        format = 'L'
        format_size = format_size / 4
    elif "long long" == datatype:
        format = 'q'
        format_size = format_size / 8
    elif "unsigned long long" == datatype:
        format = 'Q'
        format_size = format_size / 8
    elif "float" == datatype:
        format = 'f'
        format_size = format_size / 4
    elif "double" == datatype:
        format = 'd'
        format_size = format_size / 8
    elif "int" == datatype:
        format = 'i'
        format_size = format_size / 4
    elif "unsigned int" == datatype:
        format = 'I'
        format_size = format_size / 4
    else:
        raise ValueError('datatype:' + datatype)
    
    for i in range(int(format_size)):
        target_format = target_format + format

    return target_format

def read(defined, target_key, bytes_data, offset):
    # 構造体定義
    # 対象キー
    # 解析対象のバイナリ
    # 解析開始位置
    endian = defined['_Endian']
    target_def = defined[target_key]['_members']
    target_order = defined[target_key]['_order']

    # value に読込み
    read_bytes = 0
    for key in target_order:
        info = target_def[key]
        bytesize = info['_bytesize']
        format = getStructFormat(endian, info['_datatype'], bytesize)
        # 山椒のため元データにvalueを追加
        # print(key + ':' + format + "," + str(offset + read_bytes) + ' - ' + str(offset + read_bytes + bytesize))
        value = unpack(format, bytes_data[offset + read_bytes: offset + read_bytes + bytesize])
        if format[1] == 'c':
            # 文字列に変換
            value = "".join(x.decode() for x in value)
        else:
            # tupleの先頭を取得
            value = value[0]
        info['_value'] = value
        # print(info['_value'])
        read_bytes = read_bytes + bytesize

    return read_bytes

def getValue(defined, target_key, member):
    return defined[target_key]['_members'][member]['_value']

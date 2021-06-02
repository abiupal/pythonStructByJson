#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Convert Struct define in C Header file to JSON file
* Output.json as Struct defined in C Header file.

Todo:
    * Using 'typedef' and 'struct' in C Header file.
    * python struct2json.py < <C Header file>

"""
import json
import sys

is_inside_struct = False
output_json = {}
order_members = []
members = {}
offset = 0

def setEndian():
    """ set CPU Endian """
    #sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
    output_json["_Endian"] = "<" # Little for struct format

def checkStruct(line):
    """ check Struct define from C Header
    
        Args:  line string in C Header file.
    """
    global is_inside_struct
    global output_json
    global order_members
    global order_index
    global members
    global offset
    
    # print(line)
    if len(line) < 1:
        return
    sections = line.strip().split()
    #print(sections)
    if is_inside_struct == False:
        """ check to start Struct """"
        if ("typedef" in sections) and ("struct" in sections):
            is_inside_struct = True
            order_members = []
            order_index = 0
            members = {}
            offset = 0
        return
    elif sections[0] == '}':
        """ check to end struct """
        is_inside_struct = False
        struct_name = sections[1].strip(';')
        output_json[struct_name] = {}
        output_json[struct_name]['_order'] = order_members
        output_json[struct_name]['_members']= members
        return
    
    datatype = ''
    name = ''
    datasize = 1
    pos = 0
    if sections[pos] == "unsigned":
        datatype += sections[pos] + ' '
        pos = pos + 1
    # Data TYpe 
    checkTypes = ['char', 'short', 'long', 'int', 'float', 'double' ]
    types_byteSize = {'char':1, 'short':2, 'long':4, 'int':4, 'float':4, 'double':8 }
    if sections[pos] in checkTypes:
        datatype += sections[pos]
        type_datasize = types_byteSize[ sections[pos] ]
        pos = pos + 1
        vars = sections[pos].strip(';').split('[')
        name = vars[0]
        # print("vars:" + str(vars))
        if 1 < len(vars):
            # Get number of array.
            datasize = int(vars[1].strip(']'))
        datasize = datasize * type_datasize
        
        #print( datatype + ',' + name + ',' + str(datasize), ',type:' + str(type_datasize))
        
        order_members.append(name)
        members[name] = {}
        members[name]['_offset'] = offset
        members[name]['_bytesize'] = datasize
        members[name]['_datatype'] = datatype
        
        offset = offset + datasize


def main():
    setEndian()
    try:
        line = input()
        while True:
            checkStruct(line)
            line = input()
    except Exception as e:
        print(e)
        #print(output_json)
        with open("output.json", "w") as fp:
            json.dump(output_json, fp
            , ensure_ascii=False
            , indent=4
            , sort_keys=True
            , separators=(',', ': '))

if __name__ == "__main__":
    main()
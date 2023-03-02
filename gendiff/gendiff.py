#!/usr/bin/env python3
import argparse
import json
from itertools import chain

def gendiff():
    parser = argparse.ArgumentParser(
        prog='gendiff',
        description='Compares two configuration files and shows a difference.'
        )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', metavar='FORMAT',
                        help='set format of output')
    args = parser.parse_args()
    print(generate_diff(args.first_file, args.second_file))
    

def generate_diff(file1_data, file2_data):
    diff = {}
    with open(file1_data) as f1:
        with open(file2_data) as f2:
            file1_data = json.load(f1)
            file2_data = json.load(f2)
    
    file1_data = {key: value for key, value in sorted(file1_data.items())}
    file2_data = {key: value for key, value in sorted(file2_data.items())}
    for key_f1, value_f1 in file1_data.items():
        if key_f1 in file2_data:
            if value_f1 == file2_data[key_f1]:
                diff[key_f1] = value_f1
            else:
                diff['- ' + key_f1] = value_f1
                diff['+ ' + key_f1] = file2_data[key_f1]
        else:
            diff['- ' + key_f1] = value_f1
    for key in file2_data:
        if key not in file1_data:
            diff['+ ' + key] = file2_data[key]
    diff = stringify(diff)
    return diff


def stringify(value, replacer=' ', spaces_count=1):

    def iter_(current_value, depth):
        if not isinstance(current_value, dict):
            return str(current_value)

        deep_indent_size = depth + spaces_count
        deep_indent = replacer * deep_indent_size
        current_indent = replacer * depth
        lines = []
        for key, val in current_value.items():
            lines.append(f'{deep_indent}{key}: {iter_(val, deep_indent_size)}')
        result = chain("{", lines, [current_indent + "}"])
        return '\n'.join(result)

    return iter_(value, 0)



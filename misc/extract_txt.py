# pylint: disable=invalid-name
"""
Convert all non .txt file into text file under a directory

Usage:
    python misc/extract_txt.py <path_to_directory>
"""

import argparse
import os
import textract


def extra_text(path):
    return textract.process(path)

def get_file_list(path):
    file_list = []
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            _, file_extension = os.path.splitext(filename)
            if file_extension in ['.doc', '.docx', '.pdf']:
                file_list.append(os.path.join(dirpath, filename))

    return file_list

def main(path):
    file_list = get_file_list(path)
    for file in file_list:
        filename, _ = os.path.splitext(file)
        with open('{}.txt'.format(filename), 'w') as output_file:
            content = extra_text(file)
            output_file.write(content.decode())

if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('path', help='The directory to the files', default=0)
    arguments = argument_parser.parse_args()
    main(arguments.path)

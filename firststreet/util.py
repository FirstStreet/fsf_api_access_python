# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation
import logging
import ast


def read_search_items_from_file(file_name):
    """Reads the given file and pulls a list of FSIDs from the file

    Args:
        file_name (str): A file name
    Returns:
        A list of fsids
    """

    fsids = []

    with open(file_name) as fp:

        count = 1
        for line in fp:

            item = line.rstrip('\n')
            try:
                fsids.append(ast.literal_eval(item))
            except SyntaxError:
                fsids.append(line.rstrip('\n'))

            count += 1

    return fsids

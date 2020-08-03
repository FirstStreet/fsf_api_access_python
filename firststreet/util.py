# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation
import ast


def read_search_items_from_file(file_name):
    """Reads the given file and pulls a list of search_items from the file

    Args:
        file_name (str): A file name
    Returns:
        A list of search_items
    """

    search_items = []

    with open(file_name) as fp:

        count = 1
        for line in fp:

            item = line.rstrip('\n')
            try:
                search_items.append(ast.literal_eval(item))
            except SyntaxError:
                search_items.append(line.rstrip('\n'))
            except ValueError:
                if count != 1:
                    search_items.append(line.rstrip('\n'))

            count += 1

    return search_items

# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation
import logging


def read_fsid_file(file_name):
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

            try:
                fsids.append(int(line.rstrip('\n')))
                count += 1

            except ValueError:
                logging.warning("'{}' from file at line {} is not a valid fsid. This line has been skipped. "
                                "Please check the content of the file if this is unexpected.".
                                format(line.rstrip('\n'), count))

    return fsids

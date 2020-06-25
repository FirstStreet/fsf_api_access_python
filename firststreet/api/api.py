# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Standard Imports
import asyncio

# Internal Imports
import os

from firststreet.errors import InvalidArgument
from firststreet.util import read_fsid_file


class Api:
    """This class handles the calls to the API through the http class

        Attributes:
            http (Http): A http class to connect to the First Street Foundation API
        Methods:
            call_api: Creates an endpoint
        """

    def __init__(self, http):
        self._http = http

    def call_api(self, fsids, product, product_subtype, location, limit=100):
        """Receives FSIDs, a product, a product subtype, and a location to create and call an endpoint to the First
        Street Foundation API.

        Args:
            fsids (list/file): A First Street Foundation IDs or a file of First Street Foundation IDs
            product (str): The overall product to call
            product_subtype (str): The product subtype (if suitable)
            location (str/None): The location lookup type (if suitable)
            limit (int): max number of connections to make
        Returns:
            A list of JSON responses
        """
        if not isinstance(fsids, list):
            if isinstance(fsids, str):
                if os.path.isfile(os.getcwd() + "console/terminal" + fsids):
                    fsids = read_fsid_file(os.getcwd() + "/" + fsids)
                else:
                    raise InvalidArgument("File provided is not a valid file. "
                                          "Please check the file name. '{}'".format(os.path.curdir + str(fsids)))
            else:
                raise InvalidArgument("File provided is not a list or a valid file. "
                                      "Please check the file name. '{}'".format(os.path.curdir + str(fsids)))

        if not fsids:
            raise InvalidArgument(fsids)
        elif not isinstance(fsids, list):
            raise TypeError("location is not a string")

        base_url = self._http.options.get('url')
        version = self._http.version

        # Create the endpoint
        if location:
            endpoints = [("/".join([base_url, version, product, product_subtype, location, str(fsid)]), fsid,
                          product, product_subtype) for fsid in fsids]
        else:
            endpoints = [("/".join([base_url, version, product, product_subtype, str(fsid)]), fsid,
                          product, product_subtype) for fsid in fsids]

        # Asynchronously call the API for each endpoint
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self._http.endpoint_execute(endpoints, limit))

        return response

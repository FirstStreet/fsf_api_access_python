# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Standard Imports
import asyncio
import urllib.parse

# Internal Imports
import os

from firststreet.errors import InvalidArgument
from firststreet.util import read_search_items_from_file


class Api:
    """This class handles the calls to the API through the http class

        Attributes:
            http (Http): A http class to connect to the First Street Foundation API
        Methods:
            call_api: Creates an endpoint
        """

    def __init__(self, http):
        """ Init"""
        self._http = http

    def call_api(self, search_item, product, product_subtype, location=None, tile_product=None, year=None,
                 return_period=None, event_id=None, extra_param=None):
        """Receives an item, a product, a product subtype, and a location to create and call an endpoint to the First
        Street Foundation API.

        Args:
            search_item (list/file): A First Street Foundation IDs, lat/lng pair, address, or a
                file of First Street Foundation IDs
            product (str): The overall product to call
            product_subtype (str): The product subtype (if suitable)
            location (str/None): The location type (if suitable)
            tile_product (str/None): The tile product (if suitable)
            year (int/None): The year for probability depth tiles (if suitable)
            return_period (int/None): The return period for probability depth tiles (if suitable)
            event_id (int/None): The event_id for historic tiles (if suitable)
            extra_param (dict): Extra parameter to be added to the url
        Returns:
            A list of JSON responses
        """

        # Not a list. This means it's should be a file
        if not isinstance(search_item, list):

            # Check if it's a file
            if isinstance(search_item, str) and os.path.isfile(search_item):

                # Get search items from file
                search_item = read_search_items_from_file(search_item)

            else:
                raise InvalidArgument("File provided is not a list or a valid file. "
                                      "Please check the file name and path. '{}'".format(str(search_item)))

        else:

            # Check tile product
            if tile_product:
                if not all(isinstance(t, tuple) for t in search_item):
                    raise TypeError("Input must be a list of coordinates in a tuple of (z, x, y). "
                                    "Provided Arg: {}".format(search_item))

                if not all(isinstance(coord, int) for t in search_item for coord in t):
                    raise TypeError("Each coordinate in the tuple must be an integer. Provided Arg: {}"
                                    .format(search_item))

                if not all(0 < t[0] <= 18 for t in search_item):
                    raise TypeError("Max zoom is 18. Provided Arg: {}".format(search_item))

            # else:

        # Ensure for historic and adaptation the search items are EventIDs or AdaptationIDs
        if ((product == "adaptation" and product_subtype == "detail") or
            (product == "historic" and product_subtype == "event") or
            (product == "economic/avm" and product_subtype == "provider")) and \
                not all(isinstance(t, int) for t in search_item):
            raise TypeError("Input must be an integer for this product. "
                            "Provided Arg: {}".format(search_item))

        # No items found
        if not search_item:
            raise InvalidArgument(search_item)

        base_url = self._http.options.get('url')
        version = self._http.version

        # Create the endpoint
        endpoints = []
        for item in search_item:
            if location:
                endpoint = "/".join([base_url, version, product, product_subtype, location])
            elif tile_product:
                if event_id:
                    endpoint = "/".join([base_url, version, product, product_subtype, tile_product,
                                         str(event_id), "/".join(map(str, item))])
                else:
                    endpoint = "/".join([base_url, version, product, product_subtype, tile_product,
                                         str(year), str(return_period), "/".join(map(str, item))])
            else:
                endpoint = "/".join([base_url, version, product, product_subtype])

            if not tile_product:

                if not extra_param:
                    formatted_params = ""
                else:
                    formatted_params = urllib.parse.urlencode(extra_param)

                # fsid
                if isinstance(item, int):
                    endpoint = endpoint + "/{}".format(item) + "?{}".format(formatted_params)

                # lat/lng
                elif isinstance(item, tuple):
                    endpoint = endpoint + "?lat={}&lng={}&{}".format(item[0], item[1], formatted_params)

                # address
                elif isinstance(item, str):
                    endpoint = endpoint + "?address={}&{}".format(item, formatted_params)

            endpoints.append((endpoint, item, product, product_subtype))

        # Asynchronously call the API for each endpoint
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self._http.endpoint_execute(endpoints))

        return response

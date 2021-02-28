# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Standard Imports
import logging

# Internal Imports
from firststreet.api import csv_format
from firststreet.api.api import Api
from firststreet.errors import InvalidArgument
from firststreet.models.location import LocationDetailProperty, LocationDetailNeighborhood, LocationDetailCity, \
    LocationDetailZcta, LocationDetailTract, LocationDetailCounty, LocationDetailCd, \
    LocationDetailState, LocationSummaryProperty, LocationSummaryOther


class Location(Api):
    """This class receives a list of search_items and handles the creation of a location product from the request.

        Methods:
            get_detail: Retrieves a list of Location Details for the given list of IDs
            get_summary: Retrieves a list of Location Summary for the given list of IDs
        """

    def get_detail(self, search_items, location_type, csv=False, output_dir=None, extra_param=None):
        """Retrieves location detail product data from the First Street Foundation API given a list of search_items and
        returns a list of Location Detail objects.

        Args:
            search_items (list/file): A First Street Foundation IDs, lat/lng pair, address, or a
                file of First Street Foundation IDs
            location_type (str): The location lookup type
            csv (bool): To output extracted data to a csv or not
            output_dir (str): The output directory to save the generated csvs
            extra_param (dict): Extra parameter to be added to the url

        Returns:
            A list of Location Detail
        Raises:
            InvalidArgument: The location provided is empty
            TypeError: The location provided is not a string
        """

        if not location_type:
            raise InvalidArgument("No loocation type provided: {}".format(location_type))
        elif not isinstance(location_type, str):
            raise TypeError("location is not a string")

        # Get data from api and create objects
        api_datas = self.call_api(search_items, "location", "detail", location_type, extra_param=extra_param)

        if location_type == 'property':
            product = [LocationDetailProperty(api_data) for api_data in api_datas]

        elif location_type == 'neighborhood':
            product = [LocationDetailNeighborhood(api_data) for api_data in api_datas]

        elif location_type == 'city':
            product = [LocationDetailCity(api_data) for api_data in api_datas]

        elif location_type == 'zcta':
            product = [LocationDetailZcta(api_data) for api_data in api_datas]

        elif location_type == 'tract':
            product = [LocationDetailTract(api_data) for api_data in api_datas]

        elif location_type == 'county':
            product = [LocationDetailCounty(api_data) for api_data in api_datas]

        elif location_type == 'cd':
            product = [LocationDetailCd(api_data) for api_data in api_datas]

        elif location_type == 'state':
            product = [LocationDetailState(api_data) for api_data in api_datas]

        else:
            raise NotImplementedError

        if csv:
            csv_format.to_csv(product, "location", "detail", location_type, output_dir=output_dir)

        logging.info("Location Detail Data Ready.")

        return product

    def get_summary(self, search_items, location_type, csv=False, output_dir=None, extra_param=None):
        """Retrieves location summary product data from the First Street Foundation API given a list of search_items and
        returns a list of Location Summary objects.

        Args:
            search_items (list/file): A First Street Foundation IDs, lat/lng pair, address, or a
                file of First Street Foundation IDs
            location_type (str): The location lookup type
            csv (bool): To output extracted data to a csv or not
            output_dir (str): The output directory to save the generated csvs
            extra_param (dict): Extra parameter to be added to the url

        Returns:
            A list of Location Summary
        Raises:
            InvalidArgument: The location provided is empty
            TypeError: The location provided is not a string
        """

        if not location_type:
            raise InvalidArgument(location_type)
        elif not isinstance(location_type, str):
            raise TypeError("location is not a string")

        # Get data from api and create objects
        api_datas = self.call_api(search_items, "location", "summary", location_type, extra_param=extra_param)

        if location_type == "property":
            product = [LocationSummaryProperty(api_data) for api_data in api_datas]

        else:
            product = [LocationSummaryOther(api_data) for api_data in api_datas]

        if csv:
            csv_format.to_csv(product, "location", "summary", location_type, output_dir=output_dir)

        logging.info("Location Summary Data Ready.")

        return product

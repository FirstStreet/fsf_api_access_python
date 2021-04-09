# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Standard Imports
import logging

# Internal Imports
from firststreet.api import csv_format
from firststreet.api.api import Api
from firststreet.errors import InvalidArgument
from firststreet.models.economic import AVMProperty, AVMProvider, AALSummaryProperty, AALSummaryOther, NFIPPremium


class AAL(Api):
    """This class receives a list of search_items and handles the creation of an aal product from the request.

        Methods:
            get_summary: Retrieves a list of AAL Summary for the given list of IDs
        """

    def get_summary(self, search_items, location_type, csv=False, output_dir=None, extra_param=None):
        """Retrieves AAL summary product data from the First Street Foundation API given a list of search_items and
        returns a list of AAL Summary objects.

        Args:
            search_items (list/file): A First Street Foundation IDs, lat/lng pair, address, or a
                file of First Street Foundation IDs
            location_type (str): The location lookup type
            csv (bool): To output extracted data to a csv or not
            output_dir (str): The output directory to save the generated csvs
            extra_param (dict): Extra parameter to be added to the url

        Returns:
            A list of AAL Summary
        Raises:
            InvalidArgument: The location provided is empty
            TypeError: The location provided is not a string
        """

        if not location_type:
            raise InvalidArgument(location_type)
        elif not isinstance(location_type, str):
            raise TypeError("location is not a string")

        # Get data from api and create objects
        if extra_param and "depths" in extra_param:
            extra_param["depths"] = ','.join(map(str, extra_param["depths"]))

        api_datas = self.call_api(search_items, "economic/aal", "summary", location_type, extra_param=extra_param)

        product = []
        for api_data, fsid in api_datas:
            api_data["fsid"] = fsid

            if location_type == "property":
                product.append(AALSummaryProperty(api_data))
            else:
                product.append(AALSummaryOther(api_data))

        if csv:
            csv_format.to_csv(product, "economic_aal", "summary", location_type, output_dir=output_dir)

        logging.info("AAL Summary Data Ready.")

        return product


class AVM(Api):
    """This class receives a list of search_items and handles the creation of an AVM product from the request.

        Methods:
            get_avm: Retrieves a list of AVM for the given list of IDs
            get_provider: Retrieves a list of AVM providers for the given list of IDs
        """

    def get_avm(self, search_items, csv=False, output_dir=None, extra_param=None):
        """Retrieves AVM product data from the First Street Foundation API given a list of search_items and
        returns a list of AVM objects.

        Args:
            search_items (list/file): A First Street Foundation IDs, lat/lng pair, address, or a
                file of First Street Foundation IDs
            csv (bool): To output extracted data to a csv or not
            output_dir (str): The output directory to save the generated csvs
            extra_param (dict): Extra parameter to be added to the url

        Returns:
            A list of AVM
        """
        # Get data from api and create objects
        api_datas = self.call_api(search_items, "economic", "avm", "property", extra_param=extra_param)

        product = [AVMProperty(api_data) for api_data in api_datas]

        if csv:
            csv_format.to_csv(product, "economic_avm", "avm", "property", output_dir=output_dir)

        logging.info("AVM Data Ready.")

        return product

    def get_provider(self, search_items, csv=False, output_dir=None, extra_param=None):
        """Retrieves AVM provider product data from the First Street Foundation API given a list of search_items and
        returns a list of AVM provider objects.

        Args:
            search_items (list/file): A First Street Foundation IDs, lat/lng pair, address, or a
                file of First Street Foundation IDs
            csv (bool): To output extracted data to a csv or not
            output_dir (str): The output directory to save the generated csvs
            extra_param (dict): Extra parameter to be added to the url

        Returns:
            A list of AVM Provider
        """
        # Get data from api and create objects
        api_datas = self.call_api(search_items, "economic/avm", "provider", extra_param=extra_param)

        product = [AVMProvider(api_data) for api_data in api_datas]

        if csv:
            csv_format.to_csv(product, "economic_avm", "provider", output_dir=output_dir)

        logging.info("AVM Provider Data Ready.")

        return product


class Economic(Api):
    """This class receives a list of search_items and handles the creation of an economic product from the request.

        Methods:
            get_property_nfip: Retrieves a list of property nfip premiums for the given list of IDs
        """

    def get_property_nfip(self, search_items, csv=False, output_dir=None, extra_param=None):
        """Retrieves AVM product data from the First Street Foundation API given a list of search_items and
        returns a list of AVM objects.

        Args:
            search_items (list/file): A First Street Foundation IDs, lat/lng pair, address, or a
                file of First Street Foundation IDs
            csv (bool): To output extracted data to a csv or not
            output_dir (str): The output directory to save the generated csvs
            extra_param (dict): Extra parameter to be added to the url

        Returns:
            A list of property NFIP premiums
        """
        # Get data from api and create objects
        api_datas = self.call_api(search_items, "economic", "nfip", "property", extra_param=extra_param)

        product = [NFIPPremium(api_data) for api_data in api_datas]

        if csv:
            csv_format.to_csv(product, "economic", "nfip", "property", output_dir=output_dir)

        logging.info("NFIP Premium Data Ready.")

        return product

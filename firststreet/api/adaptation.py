# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Standard Imports
import logging

# Internal Imports
from firststreet.api import csv_format
from firststreet.api.api import Api
from firststreet.errors import InvalidArgument
from firststreet.models.adaptation import AdaptationDetail, AdaptationSummary


class Adaptation(Api):
    """This class receives a list of search_items and handles the creation of a adaptation product from the request.

        Methods:
            get_detail: Retrieves a list of Adaptation Details for the given list of IDs
            get_summary: Retrieves a list of Adaptation Summary for the given list of IDs
        """

    def get_detail(self, search_items, csv=False, output_dir=None, extra_param=None):
        """Retrieves adaptation detail product data from the First Street Foundation API given a list of search_items
         and returns a list of Adaptation Detail objects.

        Args:
            search_items (list/file): A First Street Foundation IDs, lat/lng pair, address, or a
                file of First Street Foundation IDs
            csv (bool): To output extracted data to a csv or not
            output_dir (str): The output directory to save the generated csvs
            extra_param (dict): Extra parameter to be added to the url

        Returns:
            A list of Adaptation Detail
        """
        # Get data from api and create objects
        api_datas = self.call_api(search_items, "adaptation", "detail", None, extra_param=extra_param)
        product = [AdaptationDetail(api_data) for api_data in api_datas]

        if csv:
            csv_format.to_csv(product, "adaptation", "detail", output_dir=output_dir)

        logging.info("Adaptation Detail Data Ready.")

        return product

    def get_detail_by_location(self, search_items, location_type, csv=False, output_dir=None, extra_param=None):
        """Retrieves adaptation detail product data from the First Street Foundation API given a list of location
        search_items and returns a list of Adaptation Detail objects.

        Args:
            search_items (list/file): A First Street Foundation IDs, lat/lng pair, address, or a
                file of First Street Foundation IDs
            location_type (str): The location lookup type
            csv (bool): To output extracted data to a csv or not
            output_dir (str): The output directory to save the generated csvs
            extra_param (dict): Extra parameter to be added to the url

        Returns:
            A list of list of Adaptation Summary and Adaptation Detail
        Raises:
            InvalidArgument: The location provided is empty
            TypeError: The location provided is not a string
        """

        if not location_type:
            raise InvalidArgument(location_type)
        elif not isinstance(location_type, str):
            raise TypeError("location is not a string")

        # Get data from api and create objects
        api_datas_summary = self.call_api(search_items, "adaptation", "summary", location_type, extra_param=extra_param)
        summary = [AdaptationSummary(api_data) for api_data in api_datas_summary]

        search_items = list(set([adaptation for sum_adap in summary if sum_adap.adaptation for
                                 adaptation in sum_adap.adaptation]))

        if search_items:
            api_datas_detail = self.call_api(search_items, "adaptation", "detail", None, extra_param=extra_param)

        else:
            api_datas_detail = [{"adaptationId": None, "valid_id": False}]

        detail = [AdaptationDetail(api_data) for api_data in api_datas_detail]

        if csv:
            csv_format.to_csv([summary, detail], "adaptation", "summary_detail", location_type,
                              output_dir=output_dir)

        logging.info("Adaptation Summary Detail Data Ready.")

        return [summary, detail]

    def get_summary(self, search_items, location_type, csv=False, output_dir=None, extra_param=None):
        """Retrieves adaptation summary product data from the First Street Foundation API given a list of
        search_items and returns a list of Adaptation Summary objects.

        Args:
            search_items (list/file): A First Street Foundation IDs, lat/lng pair, address, or a
                file of First Street Foundation IDs
            location_type (str): The location lookup type
            csv (bool): To output extracted data to a csv or not
            output_dir (str): The output directory to save the generated csvs
            extra_param (dict): Extra parameter to be added to the url

        Returns:
            A list of Adaptation Summary
        Raises:
            InvalidArgument: The location provided is empty
            TypeError: The location provided is not a string
        """

        if not location_type:
            raise InvalidArgument(location_type)
        elif not isinstance(location_type, str):
            raise TypeError("location is not a string")

        # Get data from api and create objects
        api_datas = self.call_api(search_items, "adaptation", "summary", location_type, extra_param=extra_param)
        product = [AdaptationSummary(api_data) for api_data in api_datas]

        if csv:
            csv_format.to_csv(product, "adaptation", "summary", location_type, output_dir=output_dir)

        logging.info("Adaptation Summary Data Ready.")

        return product

# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Standard Imports
import logging

# Internal Imports
from firststreet.api import csv_format
from firststreet.api.api import Api
from firststreet.errors import InvalidArgument
from firststreet.models.historic import HistoricEvent, HistoricSummary


class Historic(Api):
    """This class receives a list of search_items and handles the creation of a historic product from the request.

        Methods:
            get_event: Retrieves a list of Historic Event for the given list of IDs
            get_summary: Retrieves a list of Historic Summary for the given list of IDs
        """

    def get_event(self, search_items, csv=False, output_dir=None, extra_param=None):
        """Retrieves historic event product data from the First Street Foundation API given a list of search_items and
        returns a list of Historic Event objects.

        Args:
            search_items (list/file): A First Street Foundation IDs, lat/lng pair, address, or a
                file of First Street Foundation IDs
            csv (bool): To output extracted data to a csv or not
            output_dir (str): The output directory to save the generated csvs
            extra_param (dict): Extra parameter to be added to the url

        Returns:
            A list of Historic Event
        """

        # Get data from api and create objects
        api_datas = self.call_api(search_items, "historic", "event", None, extra_param=extra_param)
        product = [HistoricEvent(api_data) for api_data in api_datas]

        if csv:
            csv_format.to_csv(product, "historic", "event", output_dir=output_dir)

        logging.info("Historic Event Data Ready.")

        return product

    def get_events_by_location(self, search_items, location_type, csv=False, output_dir=None, extra_param=None):
        """Retrieves historic summary product data from the First Street Foundation API given a list of location
        search_items and returns a list of Historic Summary objects.

        Args:
            search_items (list/file): A First Street Foundation IDs, lat/lng pair, address, or a
                file of First Street Foundation IDs
            location_type (str): The location lookup type
            csv (bool): To output extracted data to a csv or not
            output_dir (str): The output directory to save the generated csvs
            extra_param (dict): Extra parameter to be added to the url

        Returns:
            A list of Historic Event
        Raises:
            InvalidArgument: The location provided is empty
            TypeError: The location provided is not a string
        """

        if not location_type:
            raise InvalidArgument(location_type)
        elif not isinstance(location_type, str):
            raise TypeError("location is not a string")

        # Get data from api and create objects
        api_datas = self.call_api(search_items, "historic", "summary", location_type)
        summary = [HistoricSummary(api_data) for api_data in api_datas]

        search_item = list(set([event.get("eventId") for sum_hist in summary if sum_hist.historic for
                                event in sum_hist.historic]))

        if search_item:
            api_datas_event = self.call_api(search_item, "historic", "event", None, extra_param=extra_param)

        else:
            api_datas_event = [{"eventId": None, "valid_id": False}]

        event = [HistoricEvent(api_data) for api_data in api_datas_event]

        if csv:
            csv_format.to_csv([summary, event], "historic", "summary_event", location_type, output_dir=output_dir)

        logging.info("Historic Summary Event Data Ready.")

        return [summary, event]

    def get_summary(self, search_items, location_type, csv=False, output_dir=None, extra_param=None):
        """Retrieves historic summary product data from the First Street Foundation API given a list of search_items and
        returns a list of Historic Summary objects.

        Args:
            search_items (list/file): A First Street Foundation IDs, lat/lng pair, address, or a
                file of First Street Foundation IDs
            location_type (str): The location lookup type
            csv (bool): To output extracted data to a csv or not
            output_dir (str): The output directory to save the generated csvs
            extra_param (dict): Extra parameter to be added to the url

        Returns:
            A list of Historic Summary
        Raises:
            InvalidArgument: The location provided is empty
            TypeError: The location provided is not a string
        """

        if not location_type:
            raise InvalidArgument(location_type)
        elif not isinstance(location_type, str):
            raise TypeError("location is not a string")

        # Get data from api and create objects
        api_datas = self.call_api(search_items, "historic", "summary", location_type, extra_param=extra_param)
        product = [HistoricSummary(api_data) for api_data in api_datas]

        if csv:
            csv_format.to_csv(product, "historic", "summary", location_type, output_dir=output_dir)

        logging.info("Historic Summary Data Ready.")

        return product

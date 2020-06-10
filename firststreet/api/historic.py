# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Internal Imports
from firststreet.api import csv_format
from firststreet.api.api import Api
from firststreet.errors import InvalidArgument
from firststreet.models.historic import HistoricEvent, HistoricSummary


class Historic(Api):
    """This class receives a list of fsids and handles the creation of a historic product from the request.

        Methods:
            get_event: Retrieves a list of Historic Event for the given list of IDs
            get_summary: Retrieves a list of Historic Summary for the given list of IDs
        """

    def get_event(self, fsids, csv=False):
        """Retrieves historic event product data from the First Street Foundation API given a list of FSIDs and
        returns a list of Historic Event objects.

        Args:
            fsids (list): A First Street ID
            csv (bool): To output extracted data to a csv or not
        Returns:
            A list of Historic Event
        """

        # Get data from api and create objects
        api_datas = self.call_api(fsids, "historic", "event", None)
        product = [HistoricEvent(api_data) for api_data in api_datas]

        if csv:
            csv_format.to_csv(product, "historic", "event")

        return product

    def get_summary(self, fsids, location_type, csv=False):
        """Retrieves historic summary product data from the First Street Foundation API given a list of FSIDs and
        returns a list of Historic Summary objects.

        Args:
            fsids (list): A First Street ID
            location_type (str): The location lookup type
            csv (bool): To output extracted data to a csv or not
        Returns:
            A list of Historic Summary
        """

        if not location_type:
            raise InvalidArgument(location_type)
        elif not isinstance(location_type, str):
            raise TypeError("location is not a string")

        # Get data from api and create objects
        api_datas = self.call_api(fsids, "historic", "summary", location_type)
        product = [HistoricSummary(api_data) for api_data in api_datas]

        if csv:
            csv_format.to_csv(product, "historic", "summary", location_type)

        return product

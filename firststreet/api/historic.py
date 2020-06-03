# Internal Imports
from firststreet.api.api import Api
from firststreet.errors import InvalidArgument
from firststreet.models.historic_event import HistoricEvent
from firststreet.models.historic_summary import HistoricSummary


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

        api_datas = self.call_api(fsids, "historic", "event", None)
        product = [HistoricEvent(api_data) for api_data in api_datas]

        if csv:
            self.to_csv(product)

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

        api_datas = self.call_api(fsids, "historic", "summary", location_type)
        product = [HistoricSummary(api_data) for api_data in api_datas]

        if csv:
            self.to_csv(product)

        return product

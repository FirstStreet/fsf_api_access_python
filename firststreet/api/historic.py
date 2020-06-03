# Internal Imports
from firststreet.api.api import Api
from firststreet.models.historic_event import HistoricEvent
from firststreet.models.historic_summary import HistoricSummary


class Historic(Api):
    """This class receives a list of fsids and handles the creation of a historic product from the request.

        Methods:
            get_location_detail: Retrieves a list of Location Details for the given list of IDs
            get_location_summary: Retrieves a list of Location Summary for the given list of IDs
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

    def get_summary(self, fsids, csv=False):
        """Retrieves historic summary product data from the First Street Foundation API given a list of FSIDs and
        returns a list of Historic Summary objects.

        Args:
            fsids (list): A First Street ID
            csv (bool): To output extracted data to a csv or not
        Returns:
            A list of Historic Summary
        """

        api_datas = self.call_api(fsids, "location", "summary", "property")
        product = [HistoricSummary(api_data) for api_data in api_datas]

        if csv:
            self.to_csv(product)

        return product

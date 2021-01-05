# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Internal Imports
from firststreet.models.api import Api
from firststreet.models.geometry import Geometry


class HistoricEvent(Api):
    """Creates a Historic Event object given a response

    Args:
        response (JSON): A JSON response received from the API
    """

    def __init__(self, response):
        super().__init__(response)
        self.eventId = str(response.get('eventId'))
        self.name = response.get('name')
        self.month = response.get('month')
        self.year = response.get('year')
        self.returnPeriod = response.get('returnPeriod')
        self.type = response.get('type')
        self.properties = response.get('properties')
        self.geometry = Geometry(response.get('geometry'))


class HistoricSummary(Api):
    """Creates a Historic Summary object given a response

    Args:
        response (JSON): A JSON response received from the API
    """

    def __init__(self, response):
        super().__init__(response)
        self.fsid = str(response.get('fsid'))
        self.historic = response.get('historic')

# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Internal Imports
from firststreet.models.api import Api


class Tile(Api):
    """Creates a Tile object given a response

    Args:
        response (JSON): A JSON response received from the API
    """

    def __init__(self, response):
        super().__init__(response)
        self.coordinate = response.get('coordinate')
        self.image = response.get('image')


class ProbabilityDepthTile(Tile):
    """Creates a Probability Depth Tile object given a response

    Args:
        response (JSON): A JSON response received from the API
    """

    def __init__(self, response, year, return_period):
        super().__init__(response)
        self.year = year
        self.return_period = return_period


class HistoricEventTile(Tile):
    """Creates a Historic Event Tile object given a response

    Args:
        response (JSON): A JSON response received from the API
    """

    def __init__(self, response, event_id):
        super().__init__(response)
        self.event_id = str(event_id)

# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Internal Imports
from firststreet.models.api import Api
from firststreet.models.geometry import Geometry


class AdaptationDetail(Api):
    """Creates an Adaptation Detail object given a response

    Args:
        response (JSON): A JSON response received from the API
    """

    def __init__(self, response):
        super().__init__(response)
        self.adaptationId = str(response.get('adaptationId'))
        self.name = response.get('name')
        self.type = response.get('type')
        self.scenario = response.get('scenario')
        self.conveyance = response.get('conveyance')
        self.returnPeriod = response.get('returnPeriod')
        self.serving = response.get('serving')
        self.geometry = Geometry(response.get('geometry'))


class AdaptationSummary(Api):
    """Creates an Adaptation Summary object given a response

    Args:
        response (JSON): A JSON response received from the API
    """

    def __init__(self, response):
        super().__init__(response)
        self.fsid = str(response.get('fsid'))
        self.adaptation = response.get('adaptation')
        self.properties = response.get('properties')

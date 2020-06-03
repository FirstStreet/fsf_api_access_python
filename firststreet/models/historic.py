# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Internal Imports
from firststreet.models.geometry import Geometry


class HistoricEvent:

    def __init__(self, response):
        self.eventId = response.get('eventId')
        self.name = response.get('name')
        self.month = response.get('month')
        self.year = response.get('year')
        self.returnPeriod = response.get('returnPeriod')
        self.type = response.get('type')
        self.properties = response.get('properties')
        self.geometry = Geometry(response.get('geometry'))


class HistoricSummary:

    def __init__(self, response):
        self.fsid = response.get('fsid')
        self.historic = response.get('historic')

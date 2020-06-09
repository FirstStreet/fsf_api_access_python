# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Internal Imports
from firststreet.models.geometry import Geometry


class LocationDetail:

    def __init__(self, response):
        self.fsid = response.get('fsid')


class LocationDetailProperty(LocationDetail):

    def __init__(self, response):
        super().__init__(response)
        self.fsid = response.get('fsid')
        self.streetNumber = response.get('streetNumber')
        self.route = response.get('route')
        self.city = response.get('city')
        self.zipCode = response.get('zipCode')
        self.zcta = response.get('zcta')
        self.neighborhood = response.get('neighborhood')
        self.tract = response.get('tract')
        self.county = response.get('county')
        self.cd = response.get('cd')
        self.state = response.get('state')
        self.footprintId = response.get('footprintId')
        self.elevation = response.get('elevation')
        self.fema = response.get('fema')
        if response.get('geometry'):
            self.geometry = Geometry(response.get('geometry'))


class LocationDetailNeighborhood(LocationDetail):

    def __init__(self, response):
        super().__init__(response)
        self.fsid = response.get('fsid')
        self.city = response.get('city')
        self.subtype = response.get('subtype')
        self.state = response.get('state')
        if response.get('geometry'):
            self.geometry = Geometry(response.get('geometry'))
        self.name = response.get('name')


class LocationDetailCity(LocationDetail):

    def __init__(self, response):
        super().__init__(response)
        self.fsid = response.get('fsid')
        self.lsad = response.get('lsad')
        self.zcta = response.get('zcta')
        self.neighborhood = response.get('neighborhood')
        self.state = response.get('state')
        if response.get('geometry'):
            self.geometry = Geometry(response.get('geometry'))
        self.name = response.get('name')


class LocationDetailZcta(LocationDetail):

    def __init__(self, response):
        super().__init__(response)
        self.fsid = response.get('fsid')
        self.city = response.get('city')
        self.state = response.get('state')
        if response.get('geometry'):
            self.geometry = Geometry(response.get('geometry'))
        self.name = response.get('name')


class LocationDetailTract(LocationDetail):

    def __init__(self, response):
        super().__init__(response)
        self.fsid = response.get('fsid')
        self.fips = response.get('fips')
        self.county = response.get('county')
        self.state = response.get('state')
        if response.get('geometry'):
            self.geometry = Geometry(response.get('geometry'))


class LocationDetailCounty(LocationDetail):

    def __init__(self, response):
        super().__init__(response)
        self.fsid = response.get('fsid')
        self.city = response.get('city')
        self.zcta = response.get('zcta')
        self.fips = response.get('fips')
        is_coastal = response.get('isCoastal')
        if is_coastal:
            self.isCoastal = True
        else:
            self.isCoastal = False
        self.cd = response.get('cd')
        self.state = response.get('state')
        if response.get('geometry'):
            self.geometry = Geometry(response.get('geometry'))
        self.district = response.get('district')


class LocationDetailCd(LocationDetail):

    def __init__(self, response):
        super().__init__(response)
        self.fsid = response.get('fsid')
        self.county = response.get('county')
        self.congress = response.get('congress')
        self.state = response.get('state')
        if response.get('geometry'):
            self.geometry = Geometry(response.get('geometry'))
        self.district = response.get('district')


class LocationDetailState(LocationDetail):

    def __init__(self, response):
        super().__init__(response)
        self.fsid = response.get('fsid')
        self.fips = response.get('fips')
        if response.get('geometry'):
            self.geometry = Geometry(response.get('geometry'))
        self.name = response.get('name')


class LocationSummary:

    def __init__(self, response):
        self.fsid = response.get('fsid')
        self.riskDirection = response.get('riskDirection')
        self.environmentalRisk = response.get('environmentalRisk')
        self.historic = response.get('historic')
        self.adaptation = response.get('adaptation')


class LocationSummaryProperty(LocationSummary):

    def __init__(self, response):
        super().__init__(response)
        self.floodFactor = response.get('floodFactor')


class LocationSummaryOther(LocationSummary):

    def __init__(self, response):
        super().__init__(response)
        self.properties = response.get('properties')

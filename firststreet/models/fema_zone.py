from firststreet.models.geometry import Geometry


class State:

    def __init__(self, data):
        if data:
            self.fsid = data.get('fsid')
            self.name = data.get('name')


class Firm:

    def __init__(self, data):
        self.firmId = data.get('firmId')
        self.effectiveDate = data.get('effectiveDate')
        self.preliminaryDate = data.get('preliminaryDate')
        self.state = State(data.get('state'))


class FemaZone:

    def __init__(self, response):

        self.femaID = response.get('femaID')
        self.zone = response.get('zone')
        self.floodAreaId = response.get('floodAreaId')
        self.firm = Firm(response.get('firm'))
        self.sfha = response.get('sfha')
        self.bfe = response.get('bfe')
        self.properties = response.get('properties')
        self.geometry = Geometry(response.get('geometry'))

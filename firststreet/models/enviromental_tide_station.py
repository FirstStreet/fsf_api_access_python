class EnvironmentalTideStation:

    def __init__(self, response):

        self.tideStationId = response.get('tideStationId')
        self.noaaId = response.get('noaaId')
        self.name = response.get('name')
        self.center = response.get('center')
        self.slrHistoric = response.get('slrHistoric')
        self.slrProjected = response.get('slrProjected')

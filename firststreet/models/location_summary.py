class LocationSummary:

    def __init__(self, response):

        self.fsid = response.get('fsid')
        self.floodFactor = response.get('floodFactor')
        self.riskDirection = response.get('riskDirection')
        self.environmentalRisk = response.get('environmentalRisk')
        self.properties = response.get('properties')
        self.historic = response.get('historic')
        self.adaptation = response.get('adaptation')

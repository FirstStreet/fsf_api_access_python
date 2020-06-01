class EnvironmentalSeaLevel:

    def __init__(self, response):

        self.fsid = response.get('fsid')
        self.tideStation = response.get('tideStation')

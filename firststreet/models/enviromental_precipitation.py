class EnvironmentalPrecipitation:

    def __init__(self, response):

        self.fsid = response.get("fsid")
        self.projected = response.get("projected")

class AdaptationSummary:

    def __init__(self, response):

        self.fsid = response.get('fsid')
        self.adaptation = response.get('adaptation')

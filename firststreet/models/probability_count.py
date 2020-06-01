class ProbabilityCount:

    def __init__(self, response):

        self.fsid = response.get('fsid')
        self.count = response.get('count')

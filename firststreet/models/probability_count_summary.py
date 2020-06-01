class CountSummary:

    def __init__(self, data):

        self.data = data.get('data')
        self.count = data.get('count')


class ProbabilityCountSummary:

    def __init__(self, response):

        self.fsid = response.get('fsid')
        self.count = response.get('state')
        self.count = response.get('city')
        self.count = response.get('county')
        self.count = response.get('count')
        self.count = response.get('count')

class ProbabilityCumulative:

    def __init__(self, response):

        self.fsid = response.get('fsid')
        self.cumulative = response.get('cumulative')

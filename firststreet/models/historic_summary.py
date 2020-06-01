class HistoricSummary:

    def __init__(self, response):

        self.fsid = response.get('fsid')
        self.historic = response.get('historic')



class SeriesPlot:
    def __init__(self, data):
        assert data.is_series(), "The data object must have series to use a %s" % (type(self))

        self.data = data
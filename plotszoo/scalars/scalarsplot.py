

class ScalarsPlot:
    def __init__(self, data):
        assert data.is_scalars(), "The data object must have scalars to use a %s" % (type(self))

        self.data = data
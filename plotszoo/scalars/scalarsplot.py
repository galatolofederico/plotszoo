

class ScalarsPlot:
    def __init__(self, data):
        assert "scalars" in data.data_types, "The data object must have scalars to use a %s" % (type(self))

        self.data = data
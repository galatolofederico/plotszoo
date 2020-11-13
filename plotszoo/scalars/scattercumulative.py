import numpy as np

from plotszoo.scalars import ScalarsPlot

class ScalarsScatterCumulative(ScalarsPlot):
    def __init__(self, data, x, y, cumulative_fn=np.max):
        super(ScalarsScatterCumulative, self).__init__(data)
        self.x = x
        self.y = y
        self.cumulative_fn = cumulative_fn

    def plot(self, ax):
        print(self.data.scalars.keys())
        assert False
import numpy as np

from plotszoo.scalars import ScalarsPlot

class ScalarsScatterCumulative(ScalarsPlot):
    def __init__(self, data, x, y, cumulative_fn=np.max):
        super(ScalarsScatterCumulative, self).__init__(data)
        self.x = x
        self.y = y
        self.cumulative_fn = cumulative_fn

    def plot(self, ax, sort=False):
        s = []
        for index, row in self.data.scalars.iterrows():
            s.append(dict(
                x=row[self.x],
                y=row[self.y]
            ))
        if sort:
            s = sorted(s, key=lambda e: e["x"]) 

        cumulative = []
        for e in s:
            cumulative.append(e["y"])
            e["c"] = self.cumulative_fn(cumulative)

        ax.scatter([e["x"] for e in s], [e["y"] for e in s])
        ax.plot([e["x"] for e in s], [e["c"] for e in s])
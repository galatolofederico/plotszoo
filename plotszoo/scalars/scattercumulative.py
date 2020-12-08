import numpy as np

from plotszoo.scalars import ScalarsPlot

class ScalarsScatterCumulative(ScalarsPlot):
    r"""
    Plot a scatterplot with some running cumulative function (ex. maximum, minimum, mean, sum, ...)

    Args:
        :data: :class:`plotszoo.data.DataCollection` with some scalars
        :x: Index to use as x in the scatter plot (set to ``None`` to use the :class:`DataFrame` index)
        :y: Index to use as y in the scatter plot (required)
        :cumulative_fn: Cumulative function to use (Default: ``np.max``)

    Example:

    .. literalinclude:: ../../examples/ScalarsScatterCumulative.py

    .. image:: ../../examples/images/ScalarsScatterCumulative.png
        :width: 600
    
    """
    def __init__(self, data, x, y, cumulative_fn=np.max):
        super(ScalarsScatterCumulative, self).__init__(data)
        self.x = x
        self.y = y
        self.cumulative_fn = cumulative_fn

    def plot(self, ax, sort=False, scatter=True, label=None, x_seq=False):
        r"""
        Plot the cumulative scatter plot

        Args:
            :ax: :mod:`matplotlib` ax to plot to
            :sort: Sort the x data (Default: ``False``)
            :scatter: Scatter-plot the data points (Default: ``True``) 
            :label: Label to use to plot (Default: ``None``)
            :x_seq: Use an integer sequence as x instead of the actual values (Default: ``False``)
        """
        s = []
        for index, row in self.data.scalars.iterrows():
            s.append(dict(
                x=row[self.x] if self.x is not None else index,
                y=row[self.y]
            ))
        if sort:
            s = sorted(s, key=lambda e: e["x"]) 
        
        if x_seq:
            for i, e in enumerate(s): e["x"] = i

        cumulative = []
        for e in s:
            cumulative.append(e["y"])
            e["c"] = self.cumulative_fn(cumulative)

        if scatter: ax.scatter([e["x"] for e in s], [e["y"] for e in s])
        ax.plot([e["x"] for e in s], [e["c"] for e in s], label=label)
    
        return s
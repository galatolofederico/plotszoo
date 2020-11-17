import numpy as np
import pandas as pd
import matplotlib

from plotszoo.series import SeriesPlot

class SeriesParade(SeriesPlot):
    r"""
    Plot one column from all the series

    Args:
        :data: :class:`plotszoo.data.DataCollection` with some series
        :column: The column to plot
    
    Example:

    .. literalinclude:: ../../examples/SeriesParade.py

    .. image:: ../../examples/images/SeriesParade.png
        :width: 600
    """
    def __init__(self, data, column):
        super(SeriesParade, self).__init__(data)
        self.column = column
    
    def plot(self, ax, fixed_color=None, color_fn=None, cmap="tab10"):
        r"""
        Plot the series parade

        Args:
            :ax: :mod:`matplotlib` axes to plot to
            :fixed_color: color to use for all the plots
            :color_fn: function to compute the color from the scalars
            :cmap: :mod:`matplotlib` colormap to use (Default: ``tab10``)
        """
        assert self.data.is_series(), "This plot requires series"
        if color_fn is not None: assert self.data.is_both(), "Both series and scalars are required if you specify a color_fn"
        
        cmap = matplotlib.cm.get_cmap(cmap)
        for key, series in self.data.series.items():
            color = fixed_color
            if color_fn is not None:
                color = cmap(color_fn(self.data.scalars.loc[key]))
            ax.plot(series.index, series[self.column], c=color)
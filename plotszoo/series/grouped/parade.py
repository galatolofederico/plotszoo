import numpy as np
import pandas as pd
import matplotlib

from plotszoo.series import SeriesPlot
from plotszoo.utils import confidence_interval

class GroupedSeriesParade(SeriesPlot):
    r"""
    Plot grouped mean series and their confidence intervals. Useful when working with stochastic processes. 
    This plot requires both scalars and series and requires aligned series

    Args:
        :data: :class:`plotszoo.data.DataCollection` with some series
        :groups: A list of scalar indices to group by
        :target: The series index to plot to
    
    Example:

    .. literalinclude:: ../../examples/GroupedSeriesParade.py

    .. image:: ../../examples/images/GroupedSeriesParade.png
        :width: 600
    """
    def __init__(self, data, groups, target):
        super(GroupedSeriesParade, self).__init__(data)
        self.groups = groups
        self.target = target
    
    def plot(self, ax, cmap="tab10", alpha=0.5):
        r"""
        Plot the grouped series parade

        Args:
            :ax: :mod:`matplotlib` axes to plot to
            :cmap: :mod:`matplotlib` colormap to use (Default: ``tab10``)
            :alpha: Alpha for the confidence intervals area
        """
        assert self.data.is_both(), "This plot requires both scalars and series"
        assert self.data.are_series_aligned(), "Series must be aligned"
        index = self.data.series[next(iter(self.data.series.keys()))].index
        groups_df = self.data.scalars.groupby(self.groups)
        grouped_series = dict()
        for key, group in groups_df.groups.items():
            grouped_series[key] = list()
            for elem in group:
                grouped_series[key].append(self.data.series[elem][self.target])
        
        toplot = dict()
        for key, group in grouped_series.items():
            toplot[key] = list()
            for i in index:
                val = list()
                for series in group:
                    val.append(series[i])
                toplot[key].append(dict(
                    mean=np.mean(val), 
                    ci=confidence_interval(pd.DataFrame(val))
                ))
        
        groups = list(toplot.keys())
        cmap = matplotlib.cm.get_cmap(cmap)
        norm = matplotlib.colors.Normalize(vmin=0, vmax=len(groups)-1)

        for i, group in enumerate(groups):
            mean = np.array([tp["mean"] for tp in toplot[group]])
            ci = np.array([tp["ci"][0] for tp in toplot[group]])
            
            ax.plot(index, mean, c=cmap(norm(i)))
            ax.fill_between(index, mean+ci, mean-ci, color=cmap(norm(i)), alpha=alpha)
        
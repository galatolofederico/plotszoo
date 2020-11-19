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
    
    def plot(self, ax, cmap="tab10", normalize_color=False, alpha=0.5, goal=None, goal_type="max"):
        r"""
        Plot the grouped series parade

        Args:
            :ax: :mod:`matplotlib` axes to plot to
            :cmap: :mod:`matplotlib` colormap to use (Default: ``tab10``)
            :normalize_color: Call :mod:`matplotlib` before using colormap (Default: ``False``)
            :alpha: Alpha for the confidence intervals area
            :goal: Stop plotting after a certain goal is reached for each series (Default ``None``)
            :goal_type: The goal type (``max`` or ``min``)
        """
        assert self.data.is_both(), "This plot requires both scalars and series"
        assert self.data.are_series_aligned(), "Series must be aligned"

        groups_df = self.data.scalars.groupby(self.groups)
        grouped_series = dict()

        for key, group in groups_df.groups.items():
            grouped_series[key] = list()
            for elem in group: grouped_series[key].append(self.data.series[elem][self.target])
            grouped_series[key] = pd.DataFrame(grouped_series[key]).T
            grouped_series[key] = grouped_series[key].agg([np.mean, confidence_interval], axis="columns")
        
        cmap = matplotlib.cm.get_cmap(cmap)
        norm = matplotlib.colors.Normalize(vmin=0, vmax=len(grouped_series)-1)

        for i, (group, series) in enumerate(grouped_series.items()):
            if goal is not None:
                assert goal_type in ["min", "max"]
                if goal_type == "min":
                    goal_x = np.argmax(series["mean"] <= goal)
                elif goal_type == "max":
                    goal_x = np.argmax(series["mean"] >= goal)
                
                series["mean"][goal_x+1:] = float("NaN")
                series["confidence_interval"][goal_x+1:] = float("NaN")
                
            if normalize_color:
                color = cmap(norm(i))
            else:
                color = cmap(i)
            
            ax.plot(series.index, series["mean"], c=color, label=group)
            ax.fill_between(series.index, series["mean"]+series["confidence_interval"], series["mean"]-series["confidence_interval"], color=color, alpha=alpha)
        
        return grouped_series
import numpy as np
import pandas as pd

from plotszoo.scalars import ScalarsPlot
from plotszoo.utils import confidence_interval

class GroupedScalarsBarchart(ScalarsPlot):
    r"""
    Plot a grouped mean barchart from the scalars as well as the mean confidence intervals

    Args:
        :data: :class:`plotszoo.data.DataCollection` with some scalars
        :groups: A list of indices to group by
        :targets: One or a list of targets to plot
    
    Example:

    .. literalinclude:: ../../examples/GroupedScalarsBarchart_subplots.py

    .. image:: ../../examples/images/GroupedScalarsBarchart_subplots.png
        :width: 600

    .. literalinclude:: ../../examples/GroupedScalarsBarchart.py

    .. image:: ../../examples/images/GroupedScalarsBarchart.png
        :width: 600
    """
    def __init__(self, data, groups, targets):
        super(GroupedScalarsBarchart, self).__init__(data)
        self.groups = groups
        self.targets = targets if isinstance(targets, list) else [targets]

        self.grouped_scalars = data.scalars.groupby(groups).agg({target: [np.mean, confidence_interval] for target in self.targets}) 

    def plot(self, ax, title=None, nbins=10, grid=False, yticks_fn=None, legend=None):
        r"""
        Plot the grouped mean barchart

        Args:
            :ax: :mod:`matplotlib` ax to plot to
            :title: The title of the plot (Default: ``None``)
            :nbins: Number of ticks in the x axis (Default: 10)
            :grid: Show vertical grid lines (Default: ``False``)
            :yticks_fn: A function to convert each index to text (Default: ``None``)
            :legend: Plot the legend (Default: auto)
        
        Returns:
            Grouped scalars :mod:`pandas` DataFrame
        
        """

        if legend is None: legend = len(self.targets) > 1

        means = self.grouped_scalars.loc[:, (slice(None), "mean")]
        means.columns = means.columns.droplevel(1)
        
        errors = self.grouped_scalars.loc[:, (slice(None), "confidence_interval")]
        errors.columns = errors.columns.droplevel(1)
        
        means.plot.barh(ax=ax, xerr=errors, capsize=4, xlabel="", legend=legend)

        if title is not None: ax.title.set_text(title)
        if yticks_fn is not None:
            xticks = [yticks_fn(index) for index, _ in self.grouped_scalars.iterrows()]
            ax.set_yticklabels(xticks)
        
        ax.locator_params(nbins=nbins, axis="x")
        if grid: ax.grid(which="both", axis="x", linestyle="--")

        return self.grouped_scalars
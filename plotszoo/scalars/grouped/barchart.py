import numpy as np

from plotszoo.scalars import ScalarsPlot
from plotszoo.utils import confidence_interval

class GroupedScalarsBarchart(ScalarsPlot):
    r"""
    Plot a grouped mean barchart from the scalars as well as the mean confidence intervals

    Args:
        :data: :class:`plotszoo.data.DataCollection` with some scalars
        :groups: A list of indices to group by
        :target: The index to plot
    
    Example:

    .. literalinclude:: ../../examples/GroupedScalarsBarchart.py

    .. image:: ../../examples/images/GroupedScalarsBarchart.png
        :width: 600
    """
    def __init__(self, data, groups, target):
        super(GroupedScalarsBarchart, self).__init__(data)
        self.groups = groups
        self.target = target

        self.grouped_scalars = data.scalars.groupby(groups).agg({target: [np.mean, confidence_interval]}) 

    def plot(self, ax, title=None, nbins=10, grid=False, yticks_fn=None):
        r"""
        Plot the grouped mean barchart

        Args:
            :ax: :mod:`matplotlib` ax to plot to
            :title: The title of the plot (Default: ``None``)
            :nbins: Number of ticks in the x axis (Default: 10)
            :grid: Show vertical grid lines (Default: ``False``)
            :yticks_fn: A function to convert each index to text (Default: ``None``)
        """
        self.grouped_scalars[self.target]["mean"].plot.barh(ax=ax, xerr=self.grouped_scalars[self.target]["confidence_interval"], capsize=4, xlabel="")
        if title is not None: ax.title.set_text(title)
        if yticks_fn is not None:
            xticks = [yticks_fn(index) for index, _ in self.grouped_scalars.iterrows()]
            ax.set_yticklabels(xticks)
        ax.locator_params(nbins=nbins, axis="x")
        if grid: ax.grid(which="both", axis="x", linestyle="--")
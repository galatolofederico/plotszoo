import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from plotszoo.scalars import ScalarsPlot

class ScalarsParallelCoordinates(ScalarsPlot):
    r"""
    Plot a parallel coordinates plot with respect to ``groups`` and using ``target`` as rightmost field

    Args:
        :data: :class:`plotszoo.data.DataCollection` with some scalars
        :groups: columns of ``data`` scalars to plot the data against
        :target: column of ``data``, plotted rightmost and used to color the plot
    
    Example:

    .. literalinclude:: ../../examples/ScalarsParallelCoordinates.py

    .. image:: ../../examples/images/ScalarsParallelCoordinates.png
        :width: 600
    
    """ 
    def __init__(self, data, groups, target):
        super(ScalarsParallelCoordinates, self).__init__(data)
        self.target = target
        self.groups = groups

        self.groups.append(self.target)

    def _set_ticks_for_axis(self, dim, ax, ticks):
        # TODO: custom ticks and scale for each ax
        min_val, max_val, val_range = self.min_max_range[self.groups[dim]]
        step = val_range / float(ticks-1)
        tick_labels = [round(min_val + step * i, 2) for i in range(ticks)]
        norm_min = self.norm_df[self.groups[dim]].min()
        norm_range = np.ptp(self.norm_df[self.groups[dim]])
        norm_step = norm_range / float(ticks-1)
        ticks = [round(norm_min + norm_step * i, 2) for i in range(ticks)]
        ax.yaxis.set_ticks(ticks)
        ax.set_yticklabels(tick_labels)

    def plot(self, axes, ticks=6, adjust_whitespaces=True, cmap="Blues"):
        r"""
        Plot the parallel coordinates chart

        Args:
            :axes: List of :mod:`matplotlib` axes to plot to (you must use the same number of axes and groups)
            :ticks: Number of ticks to show in the axes (Default: 6)
            :cmap: :mod:`matplotlib` colormap to use (Default: "Blues")
            :adjust_withspaces: Call ``plt.subplots_adjust(wspace=0)`` to make the plot prettier (can have side-effects) (Default: ``True``)

        """
        assert len(axes) == len(self.groups) - 1, "You must pass a list of n axes if you use n groups (axes: %d groups: %d)" % (len(axes), len(self.groups) - 1)
        
        self.norm_df = self.data.scalars.copy()

        self.min_max_range = {}
        for col in self.groups:
            serie = self.norm_df[col]
            self.min_max_range[col] = [serie.min(), serie.max(), np.ptp(serie)]
            self.norm_df[col] = np.true_divide(serie - serie.min(), np.ptp(serie))
        
        x = list(range(0, len(self.groups)))
        cmap = matplotlib.cm.get_cmap(cmap)
        norm = matplotlib.colors.Normalize(vmin=self.norm_df[self.target].min(), vmax=self.norm_df[self.target].max())

        for i, ax in enumerate(axes):
            for idx in self.norm_df.index:
                ax.plot(x, self.norm_df.loc[idx, self.groups], c=cmap(norm(self.norm_df.loc[idx, self.target])))
            ax.set_xlim([x[i], x[i+1]])

        for dim, ax in enumerate(axes):
            ax.xaxis.set_major_locator(matplotlib.ticker.FixedLocator([dim]))
            self._set_ticks_for_axis(dim, ax, ticks)
            ax.set_xticklabels([self.groups[dim]])
                

        ax = plt.twinx(axes[-1])
        dim = len(axes)
        ax.xaxis.set_major_locator(matplotlib.ticker.FixedLocator([x[-2], x[-1]]))
        self._set_ticks_for_axis(dim, ax, ticks)
        ax.set_xticklabels([self.groups[-2], self.groups[-1]])

        if adjust_whitespaces:
            plt.subplots_adjust(wspace=0)
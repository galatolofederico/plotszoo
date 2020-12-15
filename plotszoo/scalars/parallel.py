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
        self.groups = groups.copy()

        self.groups.append(self.target)

    def _set_ticks_for_axis(self, dim, ax, ticks_config):
        ticks_values = None
        tick_labels = None

        if ticks_config["type"] == "categorical":
            ticks_list = ticks_config["ticks"]
            assert type(ticks_list) is list, "When using a categorical tick, ticks must be the list of the categories"
            assert ticks_config["scale"] in ["relative", "sequential"], "When using categorical scale must be 'relative' or 'sequential'"
            
            min_val, max_val, val_range = self.min_max_range[self.groups[dim]]
            if ticks_config["scale"] == "relative":
                ticks_values = [(tick-min_val)/val_range for tick in ticks_list]
            elif ticks_config["scale"] == "sequential":
                ticks_values = [i/(len(ticks_config["ticks"])-1) for i in range(0, len(ticks_config["ticks"]))]
            
            tick_labels = ticks_list

        if ticks_config["type"] == "numeral":
            ticks_number = ticks_config["ticks"]
            min_val, max_val, val_range = self.min_max_range[self.groups[dim]]
            step = val_range / float(ticks_number-1)
            tick_labels = [round(min_val + step * i, 2) for i in range(ticks_number)]
        
            norm_min = self.norm_df[self.groups[dim]].min()
            norm_range = np.ptp(self.norm_df[self.groups[dim]])
            norm_step = norm_range / float(ticks_number-1)

            ticks_values = [round(norm_min + norm_step * i, 2) for i in range(ticks_number)]
            if ticks_config["scale"] == "logarithmic":
                tick_labels = ["1e"+str(l) for l in tick_labels]
        
        ax.yaxis.set_ticks(ticks_values)
        ax.set_yticklabels(tick_labels)

    def plot(self, axes, ticks=6, adjust_whitespaces=True, cmap="Blues", cmap_fn=None, xticks_fn=None):
        r"""
        Plot the parallel coordinates chart

        Args:
            :axes: List of :mod:`matplotlib` axes to plot to (you must use the same number of axes and groups)
            :ticks: Ticks configuration dictionary or number of ticks to show in the axes (Default: 6)
            :cmap: :mod:`matplotlib` colormap to use (Default: ``Blues``)
            :cmap_fn: Function to use instead of the :mod:`matplotlib` colormap (Default: ``None``)
            :xticks_fn: Function to create the xticks (Default: ``None``)
            :adjust_withspaces: Call ``plt.subplots_adjust(wspace=0)`` to make the plot prettier (can have side-effects) (Default: ``True``)
        
        Configuration Dictionary:

            A dictionary with a key for each ``group``. Each element is a dictionary with:
                :type: ``categorical`` or ``numeral``
                :ticks: Number of ticks if type is ``numeral``, the list of ticks in the type is ``categorical``
                :scale: The scale to use ``linear`` or ``logarithmic`` if type is ``numeral``, ``relative`` or ``sequential`` if the type is ``categorical``
            
        Configuration Dictionary Example:

            .. code:: python

                {
                    "config/train_steps": dict(type="categorical", ticks=[8, 16, 32, 64], scale="relative"),
                    "config/gamma": dict(type="categorical", ticks=[0.9, 0.99, 0.999], scale="sequential"),
                    "config/lr": dict(type="numeral", ticks=6, scale="logarithmic"),
                    "config/max_clip_norm": dict(type="numeral", ticks=6, scale="linear"),
                    "config/ent_coef": dict(type="numeral", ticks=6, scale="logarithmic"),
                    "config/vf_coef": dict(type="numeral", ticks=6, scale="linear"),
                    "config/target_entropy": dict(type="numeral", ticks=6, scale="linear"),
                    "summary/reward": dict(type="numeral", ticks=6, scale="linear")
                }

        """
        assert len(axes) == len(self.groups) - 1, "You must pass a list of n axes if you use n groups (axes: %d groups: %d)" % (len(axes), len(self.groups) - 1)
        
        if type(ticks) is dict:
            for group in self.groups: assert group in ticks, "When using a ticks dictionary an entry for each group and for the target is needed, missing entry for '%s'" % (group, )
        elif type(ticks) is int:
            ticks_number = ticks
            ticks = dict()
            for group in self.groups: ticks[group] = dict(type="numeral", ticks=ticks_number, scale="relative")
        else:
            raise Exception("ticks must be 'int' or 'dict', found '%s' instead" % (type(ticks, )))
        
        self.norm_df = self.data.scalars.copy()

        self.min_max_range = {}
        for col in self.groups:
            ticks_config = ticks[col]

            serie = self.norm_df[col]
            if ticks_config["scale"] == "linear" or ticks_config["scale"] == "relative":
                self.min_max_range[col] = [serie.min(), serie.max(), np.ptp(serie)]
                self.norm_df[col] = np.true_divide(serie - serie.min(), np.ptp(serie))
            elif ticks_config["scale"] == "sequential":
                assert ticks_config["type"] == "categorical", "'sequential' scale can be used only with type=categorical"
                self.min_max_range[col] = [0, len(ticks_config["ticks"])-1, len(ticks_config["ticks"])-1]
                for i, tick in enumerate(ticks_config["ticks"]):
                    serie = serie.replace(float(tick), i/(len(ticks_config["ticks"])-1))
                self.norm_df[col] = serie
            elif ticks_config["scale"] == "logarithmic":
                self.norm_df[col] = np.log10(self.norm_df[col])
                self.min_max_range[col] = [serie.min(), serie.max(), np.ptp(serie)]
                self.norm_df[col] = np.true_divide(serie - serie.min(), np.ptp(serie))
            else:
                raise Exception("scale can be 'relative', 'sequential', 'linear' or 'logarithmic'")
            
        
        x = list(range(0, len(self.groups)))
        if cmap_fn is None:
            cmap = matplotlib.cm.get_cmap(cmap)
            norm = matplotlib.colors.Normalize(vmin=self.norm_df[self.target].min(), vmax=self.norm_df[self.target].max())
            cmap_fn = lambda self, x: cmap(norm(x))

        for i, ax in enumerate(axes):
            for idx in self.norm_df.index:
                ax.plot(x, self.norm_df.loc[idx, self.groups], c=cmap_fn(self, self.norm_df.loc[idx, self.target]))
            ax.set_xlim([x[i], x[i+1]])

        if xticks_fn is None:
            xticks_fn = lambda x: x

        for dim, (ax, group) in enumerate(zip(axes, self.groups)):
            ticks_config = ticks[group]
            ax.xaxis.set_major_locator(matplotlib.ticker.FixedLocator([dim]))
            self._set_ticks_for_axis(dim, ax, ticks_config)
            ax.set_xticklabels([xticks_fn(label) for label in [self.groups[dim]]])
                

        ax = plt.twinx(axes[-1])
        dim = len(axes)
        ax.xaxis.set_major_locator(matplotlib.ticker.FixedLocator([x[-2], x[-1]]))
        ax.set_xticklabels([xticks_fn(label) for label in [self.groups[-2], self.groups[-1]]])

        self._set_ticks_for_axis(dim, ax, ticks[self.groups[-1]])
        
        if adjust_whitespaces:
            plt.subplots_adjust(wspace=0)
import numpy as np

from wandbplots.utils import confidence_interval

class GroupedScalarsBarchart:
    def __init__(self, data, groups, target):
        self.data = data
        self.groups = groups
        self.target = target

        self.grouped_scalars = data.scalars.groupby(groups).agg({target: [np.mean, confidence_interval]}) 

    def plot(self, ax, title=None, nbins=10, grid=False, xticks_fn=None):
        self.grouped_scalars[self.target]["mean"].plot.barh(ax=ax, xerr=self.grouped_scalars[self.target]["confidence_interval"], capsize=4, xlabel="")
        if title is not None: ax.title.set_text(title)
        if xticks_fn is not None:
            xticks = [xticks_fn(index) for index, _ in self.grouped_scalars.iterrows()]
            ax.set_yticklabels(xticks)
        ax.locator_params(nbins=nbins, axis="x")
        if grid: ax.grid(which="both", axis="x", linestyle="--")
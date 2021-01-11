import pandas as pd
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import pathlib
import os


def savefig(fig, filename, create_dir_tree=True, savefig_kwargs={}):
    r"""
    Save a :mod:`matplotlib` figure and creates the directory tree if it do not exists

    Args:
        :fig: :mod:`matplotlib` figure to save
        :filename: The figure filename
        :create_dir_tree: Create the directory tree if it does not exists (Default: ``True``)
        :savefig_kwargs: kwargs for ``plt.savefig`` (Default: ``{}``) 
    
    Example:
        >>> plotszoo.utils.savefig("./plots/nice/first.png")
    
    Creates the folders ``./plots`` and ``./plots/nice`` if they do not exists and then calls ``fig.savefig(filename, **savefig_kwargs)``
    """
    if create_dir_tree:
        path = os.path.dirname(filename)
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    fig.savefig(filename, **savefig_kwargs)


def confidence_interval(serie):
    if serie.isnull().values.any(): print("Warning skipping some NaNs")
    serie = serie.dropna()
    confidence = .95
    data = np.array(serie)
    se = scipy.stats.sem(data)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., len(data)-1)
    return h

def _walkdict(data, currentpath="", separator="/", ret=None):
    for k, v in data.items():
        level = "%s%s%s" % (currentpath, separator, k)
        if isinstance(v, dict):
            _walkdict(data=v, currentpath=level, ret=ret, separator=separator)
        else:
            ret[level] = v

def flatten_dict(d, rootpath="", separator="/"):
    fd = dict()
    _walkdict(data=d, currentpath=rootpath, ret=fd, separator=separator)
    return fd
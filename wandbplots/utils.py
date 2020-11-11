import pandas as pd
import numpy as np
import scipy.stats

def confidence_interval(serie):
    if serie.isnull().values.any(): print("Warning skipping some NaNs")
    serie = serie.dropna()
    confidence = .95
    data = np.array(serie)
    se = scipy.stats.sem(data)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., len(data)-1)
    return h

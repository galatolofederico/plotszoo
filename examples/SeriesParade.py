import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import plotszoo

num_series = 10
samples = 100
noise_level = 0.8
x = np.linspace(0, np.pi*2, samples)
types = []
series = {}
for _ in range(0, num_series):
    noisy_sin = np.sin(x) + np.random.rand(samples)*noise_level
    series[len(types)] = pd.DataFrame(noisy_sin, columns=["value"])
    types.append("sin")
    noisy_cos = np.cos(x) + np.random.rand(samples)*noise_level
    series[len(types)] = pd.DataFrame(noisy_cos, columns=["value"])
    types.append("cos")

data = plotszoo.data.DataCollection()
data.set_scalars(pd.DataFrame(types, columns=["type"]))
data.set_series(series)

fig, ax = plt.subplots()

series_parade = plotszoo.series.SeriesParade(data, "value")

series_parade.plot(ax, color_fn=lambda s: ["sin", "cos"].index(s["type"]))

fig.savefig(os.path.join(os.path.dirname(os.path.realpath(__file__)), "images/SeriesParade.png"))
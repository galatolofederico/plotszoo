import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
import plotszoo


iris = load_iris()
scalars = pd.DataFrame(data= np.c_[iris["data"], iris["target"]], columns=iris["feature_names"] + ["target"])

data = plotszoo.data.DataCollection()
data.set_scalars(scalars)

fig, axes = plt.subplots(1, len(iris["feature_names"]), sharey=False)

parallel_plot = plotszoo.scalars.ScalarsParallelCoordinates(data, iris["feature_names"], "target")

parallel_plot.plot(axes, cmap="tab10")

fig.set_size_inches(20, 10)
plt.savefig(os.path.join(os.path.dirname(os.path.realpath(__file__)), "images/ScalarsParallelCoordinates.png"))
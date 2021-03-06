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

fig, ax = plt.subplots()

yticks_fn = lambda x: iris["target_names"][int(x)]

barchart = plotszoo.scalars.grouped.GroupedScalarsBarchart(data, ["target"], iris["feature_names"])
barchart.plot(ax, title="Iris", nbins=20, grid=True, yticks_fn=yticks_fn)

fig.set_size_inches(20, 10)
fig.savefig(os.path.join(os.path.dirname(os.path.realpath(__file__)), "images/GroupedScalarsBarchart.png"))
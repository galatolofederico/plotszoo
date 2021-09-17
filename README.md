# plotszoo


**[Documentation](https://galatolofederico.github.io/plotszoo/)**


This repository contains a collection of classes to easily make some common plots as well as retrieving data from multiple sources.

This project mostly fits my needs and it doesn't want to be in any way complete nor general purpose.

Feel free to use it, submit your own plots, bugfixes, requests or ideas. Any PR is very welcomed.

*Repository under active development, braking changes may (and will) occur*

## Installation

```
pip install plotszoo
```


## Examples

### Parallel Coordinates Plot

```python
import numpy as np
import pandas as pd
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

fig.set_size_inches(30, 10)
fig.show()
```

![ScalarsParallelCoordinates](./examples/images/ScalarsParallelCoordinates.png)

### Grouped Series Parade

```python
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import plotszoo

np.random.seed(0)

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

series_parade = plotszoo.series.grouped.GroupedSeriesParade(data, ["type"], "value")

series_parade.plot(ax)

fig.show()
```

![GroupedSeriesParade](./examples/images/GroupedSeriesParade.png)


### GroupedScalarsBarchart

```python
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

fig, axes = plt.subplots(2, 2)

yticks_fn = lambda x: iris["target_names"][int(x)]
for feature, ax in zip(iris["feature_names"], axes.flatten()):
    barchart = plotszoo.scalars.grouped.GroupedScalarsBarchart(data, ["target"], feature)
    barchart.plot(ax, title=feature, nbins=20, grid=True, yticks_fn=yticks_fn)

fig.set_size_inches(20, 10)

fig.show()
```

![GroupedScalarsBarchart](./examples/images/GroupedScalarsBarchart.png)



## Contributions and license

The code is released as Free Software under the [GNU/GPLv3](https://choosealicense.com/licenses/gpl-3.0/) license. Copying, adapting e republishing it is not only consent but also encouraged. 

For any further question feel free to reach me at  [federico.galatolo@ing.unipi.it](mailto:federico.galatolo@ing.unipi.it) or on Telegram  [@galatolo](https://t.me/galatolo)

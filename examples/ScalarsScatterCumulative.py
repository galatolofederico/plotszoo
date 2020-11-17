import numpy as np
import pandas as pd
from scipy.stats import norm
import os
import matplotlib.pyplot as plt
import plotszoo

x = np.linspace(norm.ppf(0.01), norm.ppf(0.99), 20)
pdf = pd.DataFrame(norm.pdf(x)/norm.pdf(x).sum(), columns=["pdf"])

data = plotszoo.data.DataCollection()
data.set_scalars(pdf)

fig, ax = plt.subplots()

scatter_cumulative = plotszoo.scalars.ScalarsScatterCumulative(data, x=None, y="pdf", cumulative_fn=np.sum)

scatter_cumulative.plot(ax)

fig.savefig(os.path.join(os.path.dirname(os.path.realpath(__file__)), "images/ScalarsScatterCumulative.png"))
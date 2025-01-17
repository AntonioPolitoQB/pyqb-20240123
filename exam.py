# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.6
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Programming in Python
# ## Exam (simulation)
#
# You can solve the exercises below by using standard Python 3.12 libraries, NumPy, Matplotlib, Pandas, PyMC.
# You can browse the documentation: [Python](https://docs.python.org/3.12/), [NumPy](https://numpy.org/doc/stable/user/index.html), [Matplotlib](https://matplotlib.org/stable/users/index.html), [Pandas](https://pandas.pydata.org/pandas-docs/stable/user_guide/index.html), [PyMC](https://docs.pymc.io).
# You can also look at the [slides of the course](https://homes.di.unimi.it/monga/lucidi2425/pyqb00.pdf) or your code on [GitHub](https://github.com).
#
# **It is forbidden to communicate with others or "ask questions" online (i.e., stackoverflow is ok if the answer is already there, but you cannot ask a new question)**
#
# To test examples in docstrings use
#
# ```python
# import doctest
# doctest.testmod()
# ```
#

import numpy as np
import pandas as pd  # type: ignore
import matplotlib.pyplot as plt # type: ignore
import pymc as pm   # type: ignore
import arviz as az   # type: ignore

# ### Exercise 1 (max 2 points)
#
# The file [EPE.csv](./EPE.csv) (Shi, Peijian, Chen, Long, Quinn, Brady, Yu, Kexin, Miao, Qinyue, Guo, Xuchen, Lian, Meng, Gielis, Johan, & Niklas, Karl. (2023). Egg-shape data of six species of poultry. https://doi.org/10.5061/dryad.f4qrfj719) contains:
#
#
#  - `Image` saves the code of each of the 2221 eggs. The number before the hyphen represents the species code, and the number after the hyphen represents the individual code of an egg. For the number before the hyphen, 1 and 2 represent Anas platyrhynchos domesticus, and Anser cygnoides domesticus, respectively; 5, 3, 4 and 7 represent Alectoris chukar domesticus, Coturnix japonica domesticus, Gallus gallus domesticus, and Phasianus colchicus domesticus, respectively.
#
#  - `scan.length`, `scan.width` and `scan.area` represent the scanned egg length (in cm), maximum width (in cm) and planar area (in cm$^2$).
#
#  - `Albumen` represents the mass of albumen for a boiled egg in g.
#
#  - `Yolk` represents the mass of yolk for a boiled egg in g.
#
#  - `Shell` represents the mass of shell for a boiled egg in g.
#
#
#
raw = pd.read_csv('EPE.csv', sep=',')

# ### Exercise 2 (max 3 points)
#
# Add a column `Species` with the latin name of the species who produced the egg (see the description on the `Image` column of data in Exercise 1).
#

# +
raw[['Species', 'col']] = raw['Image'].str.split('-', expand=True)
raw = raw.drop(columns=['col'])

Species_arr = np.array(['Shi', 'Peijian', 'Chen', 'Long', 'Quinn', 'Brady', 'Yu', 'Kexin', 'Miao', 'Qinyue', 'Guo', 'Xuchen', 'Lian', 'Meng', 'Gielis', 'Johan', 'Niklas', 'Karl'])
Species_Id = np.array(raw['Species'])

for i in range(len(Species_Id)):
    if Species_Id[i] == '1':
        Species_Id[i] = Species_arr[0]
    elif Species_Id[i] == '2':
        Species_Id[i] = Species_arr[1]
    elif Species_Id[i] == '3':
        Species_Id[i] = Species_arr[2]
    elif Species_Id[i] == '4':
        Species_Id[i] = Species_arr[3]
    elif Species_Id[i] == '5':
        Species_Id[i] = Species_arr[4]
    elif Species_Id[i] == '6':
        Species_Id[i] = Species_arr[5]
    elif Species_Id[i] == '7':
        Species_Id[i] = Species_arr[6]

raw['Species'] = Species_Id

    
# or ,dictionary { ... : ..., , split and df[species_Id].map(dictionary)
#                  ... : ...}

# ### Exercise 3 (max 4 points)
#
# Define a function `ellipsoid_volume` that takes three floating point numbers and returns the volume of an ellipsoid given the semi-axes. The volume is given by the formula:
#
# $\frac{4}{3}\pi a b c$
#
# where $a, b, c$ are the semi-axes. For example, an ellipsoid with semi-axes of 3cm, 4cm, 5cm will have a volume approximately equal to 251.33cm$^3$.
#
#
# To get the full marks, you should declare correctly the type hints and add a test within a doctest string.

def ellipsoid_volume(a: float, b: float, c:float)->float:
    return (4/3)*np.pi*a*b*c

# ### Exercise 4 (max 4 points)
#
# Consider the ellipsoid $E$ defined by a `scan.length` (the axis $l$), a `scan.width` (an axis $w$ orthogonal to $l$) and a third axis $x$ (orthogonal to both $l$ and $w$). Then assume `scan.area` is given by $\pi\frac{scan.width}{2}\frac{x}{2}$. Add a column to the data with the values of $x$.

raw['third_axis'] = (2 * raw['scan.area'])/(raw['scan.width'] * np.pi)

# ### Exercise 5 (max 5 points)
#
# Add a column to the data with the longest axes (among `scan.width`, `scan.length`, and $x$, see previous exercise).

raw['longest_axis'] = raw[['scan.length', 'scan.width', 'third_axis']].max(axis=1)

raw['Volume'] = ellipsoid_volume(raw['scan.length'], raw['scan.width'], raw['third_axis'])
#axis 1 is for access the data
# ### Exercise 6 (max 5 points)
#
# Plot together the histograms of `scan.area` for each species.

plt.hist(raw['scan.area'], bins=50)
plt.show()

# ### Exercise 7 (max 6 points)
#
# Make a scatter plot with the volume (computed using `scan.width`, `scan.length`, and $x$ -- see Exercise 4 -- and the function defined in Exercise 3) versus the sum of Yolk and Albumen. Color the points according to the species. Pay attention to interpret correctly the numbers as axis or semi-axis.

pass

# ### Exercise 8 (max 4 points)
#
# Consider this statistical model:
#
# - the observed weight of `Albumen` together with `Yolk` is normally distributed with standard deviation $\gamma$ and a mean given by $\alpha + \beta \cdot V$ (where $V$ is the volume computed as in Exercise 7).
# - parameter $\alpha$ is normally distributed with $\mu = 0$ and $\sigma = 3$
# - parameter $\beta$ is normally distributed with $\mu = 0$ and $\sigma = 3$
# - parameter $\gamma$ is exponentially distributed with $\lambda = 1$
#
#
# Code this model with pymc, sample the model **considering only the data points with a value for both the yolk and the albumen**, and plot the summaries of the resulting estimation by using `az.plot_posterior`.
#
#

f_raw = raw.dropna(subset=['Yolk', 'Albumen'])
raw['Total_weight'] = raw['Yolk'] + raw['Albumen']
with pm.Model() as model:
    alpha = pm.Normal("alpha", mu=0, sigma=3)
    beta = pm.Normal("beta", mu=0, sigma=3)
    gamma = pm.Exponential("gamma", lam=1)
    
    mu = alpha + beta * raw['Volume']
    observed_weights = pm.Normal("observed_weights", mu=mu, sigma=gamma, observed=raw['Total_weight'])
    
    trace = pm.sample(1000, tune=1000, return_inferencedata=True)
    
az.plot_posterior(trace)
plt.show()

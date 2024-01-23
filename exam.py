# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Programming in Python
# ## Exam: January 23, 2024
#
# You can solve the exercises below by using standard Python 3.11 libraries, NumPy, Matplotlib, Pandas, PyMC.
# You can browse the documentation: [Python](https://docs.python.org/3.11/), [NumPy](https://numpy.org/doc/stable/user/index.html), [Matplotlib](https://matplotlib.org/stable/users/index.html), [Pandas](https://pandas.pydata.org/pandas-docs/stable/user_guide/index.html), [PyMC](https://docs.pymc.io).
# You can also look at the [slides of the course](https://homes.di.unimi.it/monga/lucidi2223/pyqb00.pdf) or your code on [GitHub](https://github.com).
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
#  - Image saves the code of each of the 2221 eggs. The number before the hyphen represents the species code, and the number after the hyphen represents the individual code of an egg. For the number before the hyphen, 1 and 2 represent Anas platyrhynchos domesticus, and Anser cygnoides domesticus, respectively; 5, 3, 4 and 7 represent Alectoris chukar domesticus, Coturnix japonica domesticus, Gallus gallus domesticus, and Phasianus colchicus domesticus, respectively.
#
#  - scan.length, scan.width and scan.area represent the scanned egg length (in cm), maximum width (in cm) and planar area (in cm$^2$).
#  
#  - Albumen represents the mass of albumen for a boiled egg in g.
#  
#  - Yolk represents the mass of yolk for a boiled egg in g.
#  
#  - Shell represents the mass of shell for a boiled egg in g. 
#
#
#

data = pd.read_csv('EPE.csv')
data.head()

# ### Exercise 2 (max 3 points)
#
# Add a column `Species` with the latin name of the species who produced the egg (see the description on the Image column of data).
#

# +
SPECIES = {
        '1': 'Anas platyrhynchos domesticus', 
        '2': 'Anser cygnoides domesticus',
        '5': 'Alectoris chukar domesticus', 
        '3': 'Coturnix japonica domesticus', 
        '4': 'Gallus gallus domesticus',
        '7': 'Phasianus colchicus domesticus'
}


data['Species'] = data['Image'].str.split('-').apply(lambda s: SPECIES[s[0]])


# -

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

def ellipsoid_volume(a: float, b: float, c: float) -> float:
    """Return the volume of an ellipsoid with semi-axis a, b, c
    
    >>> abs(ellipsoid_volume(3., 4., 5.) - 251.33) < 10e-3
    True
    """
    assert a > 0 and b > 0 and c > 0
    return (4/3)*np.pi*a*b*c


# ### Exercise 4 (max 4 points)
#
# Consider the ellipsoid $E$ defined by a `scan.length` (the axis $l$), a `scan.width` (an axis $w$ orthogonal to $l$) and a third axis $x$ (orthogonal to both $l$ and $w$). Then assume `scan.area` is given by $\pi\frac{scan.width}{2}\frac{x}{2}$. Add a column to the data with the values of $x$. 

data['x'] = 4*data['scan.area']/(np.pi*data['scan.width'])

# ### Exercise 5 (max 5 points)
#
# Add a column to the data with the longest axes (among `scan.width`, `scan.length`, and $x$, see previous exercise).

data['longest'] = data[['scan.width', 'scan.length', 'x']].apply(lambda t: max(t), axis=1)

assert (data['longest'] >= data['x']).all() and (data['longest'] >= data['scan.width']).all() and (data['longest'] >= data['scan.length']).all()

# ### Exercise 6 (max 5 points)
#
# Plot together the histograms of `scan.area` for each species.

fig, ax = plt.subplots(1)
for s in data['Species'].unique():
    ax.hist(data[data['Species'] == s]['scan.area'], density=True, label=s)
ax.set_title('Planar area of eggs')
_ = ax.legend()

# ### Exercise 7 (max 6 points)
#
# Make a scatter plot with the volume (computed using `scan.width`, `scan.length`, and $x$ -- see Exercise 4 -- and the function defined in Exercise 3) versus the sum of Yolk and Albumen. Color the points according to the species. Pay attention to interpret correctly the numbers as axis or semi-axis.

data['volume'] = data[['scan.width', 'scan.length','x']].apply(lambda t: ellipsoid_volume(t[0]/2, t[1]/2, t[2]/2), axis=1)

# +
fig, ax = plt.subplots(1)

for s in data['Species'].unique():
    view = data[data['Species'] == s]
    ax.scatter(view['volume'], view['Yolk'] + view['Albumen'], label=s)
ax.set_xlabel('Volume (cm$^3$)')
ax.set_ylabel('Yolk + Albumen (g)')
_ = ax.legend()
# -

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

# +
data = data[~data['Albumen'].isnull() & ~data['Yolk'].isnull()]

with pm.Model() as model:
    
    alpha = pm.Normal('alpha', mu=0, sigma=1)
    beta = pm.Normal('beta', mu=0, sigma=1)
    gamma = pm.Exponential('gamma', lam=1)
    
    content = pm.Normal('content', sigma=gamma, mu=alpha + beta*data['volume'], observed=data['Albumen']+data['Yolk'])
# -

with model:
    
    itrace = pm.sample(random_seed=42)

_ = az.plot_posterior(itrace, var_names=['alpha', 'beta', 'gamma'])

az.summary(itrace)



# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Programming in Python
# ## Exam: July 5, 2023
#
# You can solve the exercises below by using standard Python 3.10 libraries, NumPy, Matplotlib, Pandas, PyMC.
# You can browse the documentation: [Python](https://docs.python.org/3.10/), [NumPy](https://numpy.org/doc/stable/user/index.html), [Matplotlib](https://matplotlib.org/stable/users/index.html), [Pandas](https://pandas.pydata.org/pandas-docs/stable/user_guide/index.html), [PyMC](https://docs.pymc.io).
# You can also look at the [slides of the course](https://homes.di.unimi.it/monga/lucidi2223/pyqb00.pdf) or your code on [GitHub](https://github.com).
#
# **It is forbidden to communicate with others.**
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

pass

# ### Exercise 2 (max 3 points)
#
# Add a column `Species` with the latin name of the species who produced the egg (see the description on the Image column of data).
#

pass

# ### Exercise 3 (max 7 points)
#
# Define a function `ellipsoid_volume` that takes three floating point numbers and returns the volume of an ellipsoid given the semi-axes. The volume is given by the formula:
#
# $\frac{4}{3}\pi a b c$ 
#
# where $a, b, c$ are the semi-axes. For example, an ellipsoid with semi-axes of 3cm, 4cm, 5cm will have a volume approximately equal to 251.33cm$^3$.
#
#
# To get the full marks, you should declare correctly the type hints and add a test within a doctest string.

pass

# +
# You can test your docstrings by uncommenting the following two lines

# import doctest
# doctest.testmod()
# -

# ### Exercise 4 (max 4 points)
#
# Consider the ellipsoid $E$ defined by a `scan.length` (the axis $l$), a `scan.width` (an axis $w$ orthogonal to $l$) and a third axis $x$ (orthogonal to both $l$ and $w$). Then assume `scan.area` is given by $\pi\frac{scan.width}{2}\frac{x}{2}$. Add a column to the data with the values of $x$. 

pass

# ### Exercise 5 (max 4 points)
#
# Add a column to the data with the longest axes (among `scan.width`, `scan.length`, and $x$, see previous exercise).

pass

# ### Exercise 6 (max 4 points)
#
# Plot together the histograms of `scan.area` for each species.

pass

# ### Exercise 7 (max 4 points)
#
# Make a scatter plot with the volume (computed using `scan.width`, `scan.length`, and $x$ -- see Exercise 4 -- and the function defined in Exercise 3) versus the sum of Yolk and Albumen. Color the points according to the species. Pay attention to interpret correctly the numbers as axis or semi-axis.

pass

# ### Exercise 8 (max 5 points)
#
# Consider this statistical model:
#
# - a parameter $\alpha$ is normally distributed with $\mu = 0$ and $\sigma = 1$ 
# - a parameter $\beta$ is normally distributed with $\mu = 1$ and $\sigma = 2$ 
# - a parameter $\gamma$ is exponentially distributed with $\lambda = 1$
# - the observed `Yolk` (computed as in exercise 7) is normally distributed with standard deviation $\gamma$ and a mean given by $\alpha + \beta \cdot V$ (where $V$ is the volume computed as in Exercise 7).
#
# Code this model with pymc, sample the model, and plot the summary of the resulting estimation by using `az.plot_posterior`.
#
#
#
#

pass


# %%
"""
Things to experiment with:
1. Number of features (what happens to variance?)
2. Action sampling strategy
"""
import numpy as np
import matplotlib.pyplot as plt

sigma = 0.1

# Define problem
## get lower and upper
l = np.random.rand()*2
u = l + np.random.rand()*2 + 1

## get some parameters for f
peak_position = (u+l)/2 + (u-l) * (np.random.rand()-0.5)/2
width = (u-l)/2 * (1 + np.random.rand())/2
scale = 0.5 + np.random.rand()

def f_of_a(a):
    """
    Blackbox implementation of f(a)
    """
    ## get params of true function
    ## define f as inline
    return scale * np.exp(-(a-peak_position)**2/2/width)
    ## define sampling process as inline

def get_y_given_a(a):
    """
    Blackbox implementation of P(.|a)
    """
    if hasattr(a, "__len__"):
        return f_of_a(a) + np.random.normal(0, sigma, size=a.shape)
    return f_of_a(a) + np.random.normal(0, sigma)

####################################################################

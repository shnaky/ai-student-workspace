import numpy as np
import matplotlib.pyplot as plt


def regression_based_on_data(l, u, a, y):
    """
    Please modify the body of this function according to the description in exercise 2.1
    """
    # Debug print
    # print(
    #     """
    # lower bound: {}\n
    # upper bound: {}\n
    # actions a  : {}\n
    # output y   : {}\n
    # """.format(
    #         l, u, a, y
    #     )
    # )

    # linear model (weight w is the slope with LSE)
    a = a.reshape(a.size, 1)
    y = y.reshape(y.size, 1)
    # polynomial degree
    F = 3

    f, w = regression(F, a, y)
    # plot_regression(a, y, f)
    maxima = find_maxima(l, u, f, F, w)
    return maxima


def regression(F, a, y):
    # build matrix A (nxF) with polynomial features
    A = np.zeros((a.size, F))
    for i in range(a.size):
        for j in range(F):
            A[i][j] = a[i] ** j

    # weight vector of the polynomials (coefficients)
    w = np.linalg.inv(A.T @ A) @ A.T @ y

    # return polynomial function of degree F and the weights
    return get_poly_function(F, w, a), w


def get_poly_function(order, coeff, x):
    f = 0
    for i in range(order):
        f += coeff[i] * (x**i)
    return f


def find_maxima(l, u, f, F, w):
    sample = np.random.uniform(low=l, high=u, size=1000)
    poly = get_poly_function(F, w, sample)
    return sample[np.argmax(poly)]


def plot_regression(a, y, f):

    plt.plot(a, f)
    plt.scatter(a, y)
    plt.xlabel("a")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()

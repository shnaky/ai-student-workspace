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
l = np.random.rand() * 2
u = l + np.random.rand() * 2 + 1

## get some parameters for f
peak_position = (u + l) / 2 + (u - l) * (np.random.rand() - 0.5) / 2
width = (u - l) / 2 * (1 + np.random.rand()) / 2
scale = 0.5 + np.random.rand()


def f_of_a(a):
    """
    Blackbox implementation of f(a)
    """
    ## get params of true function
    ## define f as inline
    return scale * np.exp(-((a - peak_position) ** 2) / 2 / width)
    ## define sampling process as inline


def get_y_given_a(a):
    """
    Blackbox implementation of P(.|a)
    """
    if hasattr(a, "__len__"):
        return f_of_a(a) + np.random.normal(0, sigma, size=a.shape)
    return f_of_a(a) + np.random.normal(0, sigma)


####################################################################
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


def plot_regression(a, y, f):

    plt.plot(a, f)
    plt.scatter(a, y)
    plt.xlabel("a")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()


# sample count
n = 1000
# bootstrap count
B = 10
a = np.random.uniform(l, u, n)
k = n
y = get_y_given_a(a)
y_real = f_of_a(a)
# print(y_real)
D = np.asarray(list(zip(a, y)))
f_estimated = np.zeros((B, k), dtype=float)
D_sorted = np.sort(D, axis=0)
real_f, real_w = regression(3, a, f_of_a(a))
plot_regression(a, f_of_a(a), real_f)

# print(real_f)

# print(
#     """
#         a: {}\n
#         y: {}\n
#         D: {}\n
#         """.format(
#         a, y, D
#     )
# )
for b in range(10):
    np.random.shuffle(D)
    # print("D shuffled: {}\n {}".format(b, D))
    # print(D[:, 0])
    f_b_k, w = regression(2, D[:, 0], D[:, 1])
    f_estimated[b] += f_b_k
# print(f_estimated)
f_bootstrap_estimate = np.sum(f_estimated, axis=0) / B
f_k_variance_estimate = np.sum((f_estimated - f_bootstrap_estimate) ** 2, axis=0) / (
    B - 1
)
# plot_regression(D[:, 0], D[:, 1], real_f)

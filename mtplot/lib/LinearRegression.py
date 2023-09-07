import numpy as np


def compute_cost(x, y, theta=[[0], [0]]):
    m = y.size

    # linear hypothesis
    h = x.dot(theta)
    # non vectorized implementation
    J = 1 / (2 * m) * np.sum(np.square(h - y))

    # vectorized implementation
    # J = 1/(2*m)*((h-y).T.dot(h-y))

    return (J)


def gradient_descent(x, y, alpha=0.001, iteration=20000, theta=[[0], [0]]):
    m = y.size
    J = []

    for i in range(0, iteration):
        h = x.dot(theta)
        # theta = theta - (alpha/m)*np.sum((h-y)*x, axis=0).reshape((2,1))
        theta = theta - (alpha / m) * np.dot(x.T, h - y)
        """theta[0] = theta[0] - (alpha/m)*np.sum(h-y)
        theta[1] = theta[1] - (alpha/m)*np.sum(((h-y).T*x[:,1]))"""
        J.append(compute_cost(x, y, theta))

    return J, theta

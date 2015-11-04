# -*- coding: utf-8 -*-

"""Functions to generate time series of some popular chaotic systems.

Parameters and initial conditions have been taken from Sprott (2003).
"""


from __future__ import division

import numpy as np

from numpy import fft
from scipy.integrate import odeint


def henon(length=10000, x0=None, a=1.4, b=0.3, discard=500):
    """Generate time series using the Henon map.

    Generates time series using the Henon map.

    Parameters
    ----------
    length : int, optional (default = 10000)
        Length of the time series to be generated.
    x0 : array, optional (default = random)
        Initial condition for the map.
    a : float, optional (default = 1.4)
        Constant ``a`` in the Henon map.
    b : float, optional (default = 0.3)
        Constant ``b`` in the Henon map.
    discard : int, optional (default = 500)
        Number of steps to discard in order to eliminate transients.

    Returns
    -------
    x : ndarray, shape ``(length, 2)``
        Array containing points in phase space.
    """
    x = np.empty((length + discard, 2))

    if not x0:
        x[0] = (0.0, 0.9) + 0.1 * (-1 + 2 * np.random.random(2))
    else:
        x[0] = x0

    for i in range(1, length + discard):
        x[i] = (1 - a * x[i - 1][0] ** 2 + b * x[i - 1][1], x[i - 1][0])

    return x[discard:]


def ikeda(length=10000, x0=None, alpha=6.0, beta=0.4, gamma=1.0, mu=0.9,
          discard=500):
    """Generate time series from the Ikeda map.

    Generates time series from the Ikeda map.

    Parameters
    ----------
    length : int, optional (default = 10000)
        Length of the time series to be generated.
    x0 : array, optional (default = random)
        Initial condition for the map.
    alpha : float, optional (default = 6.0)
        Constant ``alpha`` in the Ikeda map.
    beta : float, optional (default = 0.4)
        Constant ``beta`` in the Ikeda map.
    gamma : float, optional (default = 1.0)
        Constant ``gamma`` in the Ikeda map.
    mu : float, optional (default = 0.9)
        Constant ``mu`` in the Ikeda map.
    discard : int, optional (default = 500)
        Number of steps to discard in order to eliminate transients.

    Returns
    -------
    x : ndarray, shape ``(length, 2)``
        Array containing points in phase space.
    """
    x = np.empty((length + discard, 2))

    if not x0:
        x[0] = 0.1 * (-1 + 2 * np.random.random(2))
    else:
        x[0] = x0

    for i in range(1, length + discard):
        phi = beta - alpha / (1 + x[i - 1][0] ** 2 + x[i - 1][1] ** 2)
        x[i] = (gamma + mu * (x[i - 1][0] * np.cos(phi) - x[i - 1][1] *
                np.sin(phi)),
                mu * (x[i - 1][0] * np.sin(phi) + x[i - 1][1] * np.cos(phi)))

    return x[discard:]


def lorenz(length=10000, x0=None, sigma=10.0, beta=8.0/3.0, rho=28.0,
           step=0.001, sample=0.03, discard=1000):
    """Generate time series using the Lorenz system.

    Generates time series using the Lorenz system.

    Parameters
    ----------
    length : int, optional (default = 10000)
        Length of the time series to be generated.
    x0 : array, optional (default = random)
        Initial condition for the flow.
    sigma : float, optional (default = 10.0)
        Constant ``sigma`` of the Lorenz system.
    beta : float, optional (default = 8.0/3.0)
        Constant ``beta`` of the Lorenz system.
    rho : float, optional (default = 28.0)
        Constant ``rho`` of the Lorenz system.
    step : float, optional (default = 0.001)
        Approximate step size of integration.
    sample : int, optional (default = 0.03)
        Sampling step of the time series.
    discard : int, optional (default = 1000)
        Number of samples to discard in order to eliminate transients.

    Returns
    -------
    t : array
        The time values at which the points have been sampled.
    x : ndarray, shape ``(length, 3)``
        Array containing points in phase space.
    """
    def _lorenz(x, t):
        return [sigma * (x[1] - x[0]), x[0] * (rho - x[2]) - x[1],
                x[0] * x[1] - beta * x[2]]

    if not x0:
        x0 = (0.0, -0.01, 9.0) + 0.25 * (-1 + 2 * np.random.random(3))

    sample = int(sample / step)
    t = np.linspace(0, (sample * (length + discard)) * step,
                    sample * (length + discard))

    return (t[discard * sample::sample],
            odeint(_lorenz, x0, t)[discard * sample::sample])


def mackey_glass(length=10000, x0=None, a=0.2, b=0.1, c=10.0, tau=23.0,
                 n=1000, sample=0.46, discard=250):
    """Generate time series using the Mackey-Glass equation.

    Generates time series using the discrete approximation of the
    Mackey-Glass delay differential equation described in Grassberger &
    Procaccia (1983).

    Parameters
    ----------
    length : int, optional (default = 10000)
        Length of the time series to be generated.
    x0 : array, optional (default = random)
        Initial condition for the discrete map.  Should be of length `n`.
    a : float, optional (default = 0.2)
        Constant ``a`` in the Mackey-Glass equation.
    b : float, optional (default = 0.1)
        Constant ``b`` in the Mackey-Glass equation.
    c : float, optional (default = 10.0)
        Constant ``c`` in the Mackey-Glass equation.
    tau : float, optional (default = 23.0)
        Time delay in the Mackey-Glass equation.
    n : int, optional (default = 1000)
        The number of discrete steps into which the interval between
        ``t`` and ``t + tau`` should be divided.  This results in a time
        step of ``tau/n`` and an ``n + 1`` dimensional map.
    sample : float, optional (default = 0.46)
        Sampling step of the time series.  It is useful to pick something
        between ``tau/100`` and ``tau/10``, with ``tau/sample`` being a
        factor of `n`.  This will make sure that there are only whole
        number indices.
    discard : int, optional (default = 250)
        Number of n-steps to discard in order to eliminate transients.
        A total of ``n*discard`` steps will be discarded.

    Returns
    -------
    x : array
        Array containing the time series.
    """
    sample = int(n * sample / tau)
    grids = n * discard + sample * length
    x = np.empty(grids)

    if not x0:
        x[:n] = 0.5 + 0.05 * (-1 + 2 * np.random.random(n))
    else:
        x[:n] = x0

    A = (2 * n - b * tau) / (2 * n + b * tau)
    B = a * tau / (2 * n + b * tau)

    for i in range(n - 1, grids - 1):
        x[i + 1] = A * x[i] + B * (x[i - n] / (1 + x[i - n] ** c) +
                                   x[i - n + 1] / (1 + x[i - n + 1] ** c))
    return x[n * discard::sample]


def roessler(length=10000, x0=None, a=0.15, b=0.20, c=10.0, step=0.001,
             sample=0.1, discard=1000):
    """Generate time series for the Rössler system.

    Generates time series for the Rössler system.

    Parameters
    ----------
    length : int, optional (default = 10000)
        Length of the time series to be generated.
    x0 : array, optional (default = random)
        Initial condition for the flow.
    a : float, optional (default = 0.15)
        Constant ``a`` in the Röessler system.
    b : float, optional (default = 0.20)
        Constant ``b`` in the Röessler system.
    c : float, optional (default = 10.0)
        Constant ``c`` in the Röessler system.
    step : float, optional (default = 0.001)
        Approximate step size of integration.
    sample : int, optional (default = 0.1)
        Sampling step of the time series.
    discard : int, optional (default = 1000)
        Number of samples to discard in order to eliminate transients.

    Returns
    -------
    t : array
        The time values at which the points have been sampled.
    x : ndarray, shape ``(length, 3)``
        Array containing points in phase space.
    """
    def _roessler(x, t):
        return [-(x[1] + x[2]), x[0] + a * x[1], b + x[2] * (x[0] - c)]

    sample = int(sample / step)
    t = np.linspace(0, (sample * (length + discard)) * step,
                    sample * (length + discard))

    if not x0:
        x0 = (-9.0, 0.0, 0.0) + 0.25 * (-1 + 2 * np.random.random(3))

    return (t[discard * sample::sample],
            odeint(_roessler, x0, t)[discard * sample::sample])
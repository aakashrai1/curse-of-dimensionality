# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 01:46:07 2018
@author: akash
"""

import random
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.distance import pdist as distance_cal

FEATURE_MIN_VALUE = 1
FEATURE_MAX_VALUE = 100
NUMBER_OF_PAIRS = 100000

def generatePoints(n, d):
    """
    Random points generator which generator n number of points of d dimensions
    Returns a List[List]
    """
    random.seed(1994)
    _data = []
    for i in range(n):
        _featureVal = []
        for j in range(d):
            _featureVal.append(random.randrange(FEATURE_MIN_VALUE, FEATURE_MAX_VALUE))
        _data.append(_featureVal)
    return _data


def euclideanDistance(points):
    """
    Calculates Maximum and Minimum Euclidean distance between n number of points
    Returns (MaxDistance, MinDistance)
    """
    distance = distance_cal(points, metric = 'euclidean')
    return (distance.max(), distance.min())


def l1normDistance(points):
    """
    Calculates Maximum and Minimum L1 Norm distance between n number of points
    Returns (MaxDistance, MinDistance)
    """
    distance = distance_cal(points, metric = 'cityblock')
    return (distance.max(), distance.min())


def calculateMaxMinDistance(data, _type=2):
    """
    Generic function to calculate distance between points
    Returns (MaxDistance, MinDistance)
    """
    if (_type == 1):
        return l1normDistance(data)
    else:
        return euclideanDistance(data)


def plot(x, y, z, name = '1'):
    """
    Function to plot a 3D graph
    """
    fig = plt.figure(figsize=(9,6))
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_trisurf(x, y, z, cmap= 'magma', antialiased=True)
    # Add labels
    ax.set_xlabel('Number of dimensions')
    ax.set_ylabel('Number of points')
    ax.set_zlabel('Gamma Value')
    # Add a color bar legend
    fig.colorbar(surf, shrink=0.7, aspect=12)
    plt.title('3d surface graph using l{} norm to calculate distances'.format(name))
    fig.savefig('fig_{}.png'.format(name), dpi=200)
    plt.show()


def run():
    """
    Driver function which generates 1 lac random n and d pairs to demonstrate dimentionality effects
    on distance between n number of points
    """
    # Generating random n and d pairs
    random.seed(1994)

    numPoints = [random.randrange(100, 1000) for i in range(NUMBER_OF_PAIRS)]
    dimensions = [random.randrange(3, 100) for i in range(NUMBER_OF_PAIRS)]
    gamma_dn1 = []
    gamma_dn2 = []

    for i, j in zip(numPoints, dimensions):
        # Using L2 Norm
        maxDistance, minDistance = calculateMaxMinDistance(generatePoints(i, j), _type=2)
        if (minDistance != 0):
            gamma_dn2.append(float(format(math.log((maxDistance - minDistance) / minDistance), '.2f')))
        else:
            gamma_dn2.append(0)

        # Using L1 Norm
        maxDistance1, minDistance1 = calculateMaxMinDistance(generatePoints(i, j), _type=1)
        if (minDistance1 != 0):
            gamma_dn1.append(float(format(math.log((maxDistance1 - minDistance1) / minDistance1), '.2f')))
        else:
            gamma_dn1.append(0)

    # Plotting the graphs
    plot(dimensions, numPoints, gamma_dn2, '2')
    plot(dimensions, numPoints, gamma_dn1, '1')


run()

"""
From the graph plot, we can visualize that gamma (d, n) value changes with respect to the number of dimensions,
as it is asserted in the problem. We can identify a curve which represents a high normalized value when in low dimensions
and low values when in very high dimensions. From the perspective of the number of points the curve is visible
as a smooth surface and remains constant with respect to dimensions and gamma (d, n).	
"""

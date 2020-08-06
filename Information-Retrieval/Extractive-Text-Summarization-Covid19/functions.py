"""Algebraic Calculations for PageRank

The functions in this simple module are to be used for graph creation
(for edge weights) and calculation of PageRank scores. 

This file can also be imported as a module and contains the following
functions:

    * cos_sim() - Calculates cosine-similarity between given two numpy
    arrays

    * find_steady_states() - Finds final probability vector while 
    performing PageRank

    * calc_error() - Returns the Eucledian-norm of the change in
    probability vector after iterations
"""

import numpy as np

def cos_sim(x:np.ndarray, y:np.ndarray) -> float :
    dot_product = np.dot(x, y)
    norm_x = np.linalg.norm(x)
    norm_y = np.linalg.norm(y)
    if norm_x == 0 or norm_y == 0 : return 0
    similarity = dot_product / (norm_x * norm_y)
    return similarity


def find_steady_states(x:np.ndarray, P:np.ndarray, epsilon=1e-5) -> np.ndarray:
    error = 100
    while error > epsilon:
        updated_x = np.dot(x, P)
        error = calc_error(updated_x-x)
        x = updated_x
    return x


def calc_error(x_change:np.ndarray):
    norm = np.dot(x_change, x_change.T)
    return norm


    



import itertools
import numpy as np
import math

def random_vectors(k, n):
    '''
    Generate a random number of n-dimensional orthonormal vectors uniformly on a hypersphere
    Exploit method of Muller mentioned in this blog under method #3
    http://extremelearning.com.au/how-to-generate-uniformly-random-points-on-n-spheres-and-n-balls/
    @param k number of vectors
    @param n dimension of the vector
    '''
    vectors = []
    for _ in range(k):
        v = np.random.normal(size=n)
        norm = np.linalg.norm(v)
        if norm > 0.0:
            vectors.append(list(v / norm))
    return vectors
def abs_inner(x):
    '''
    Absolute Value of the inner product
    '''
    return np.abs(np.inner(*x))
    
def worst_dot(samples):
    '''
    Calculate the max pairwise dot product of a set of vectors
    @param samples The set of vectors
    '''
    return max(map(abs_inner, itertools.combinations(samples, 2)))


def worst_angle(samples):
    '''
    Calculate the minimum angle of a set of vectors in degrees
    @param samples The set of vectors
    '''
    return math.acos(worst_dot(samples)) / math.pi * 180
import itertools

import numpy


def dedup(x):
    '''
    This function removes antipodal points from a set of vectors. The constant epsilon
    is used as a threshold since due to round off error, some antipodal points might not
    be exactly the negative of its counterpart
    '''

    epsilon = 0.001

    def is_neg(x, y):
        sum = 0.0
        for x0, y0 in zip(x, y):
            sum += (x0 + y0) ** 2
        return sum < epsilon

    def has_neg(x, list_):
        for y in list_:
            if is_neg(x, y):
                return True
        return False

    out = []
    for each in x:
        if not has_neg(each, out):
            out.append(each)
    return out


def parse_basis(in_):
    '''
    This function takes the sphere codes encoded in the format for neilsloane.com and parses
    out the file and removes antipodal points to net a quasiorthogonal set
    '''
    if type(in_) != list:
        in_ = in_.split('\n')
    y = map(lambda x: x.strip().split(), in_)
    return dedup([list(map(lambda x: float(x), l)) for l in y if l])


def parse_sphere(in_):
    '''
    This function takes the sphere codes encoded in the format for neilsloane.com and parses
    out the file.
    '''
    all = in_.strip().split('\n')
    out = []
    step = 3
    for idx in range(0, len(all), step):
        out.append([float(all[idx + i]) for i in range(0, step)])
    return out


def normalize(vectors):
    ''' This normalizes a set of vectors so their length is 1
    '''
    norms = numpy.apply_along_axis(numpy.linalg.norm, 1, vectors)
    return (vectors.T / norms).T


def hadamard(width, rank):
    ''' This enumerates all hadamard vectors (vectors of -1, 0, and 1) the width represents
    the total vector dimension, rank represents the number of non-zero entries per vector
    '''

    def vectorize(x):
        output = []
        for each in range(0, 2 ** rank):
            out = [0] * width
            for slot in range(0, rank):
                out[x[slot]] = 1 if each >> slot & 1 else -1
            output.append(out)
        return output

    combo = itertools.combinations(range(0, width), rank)
    out = []
    for each in map(vectorize, combo):
        out += each
    return out

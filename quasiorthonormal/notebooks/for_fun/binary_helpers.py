import numpy
def binary(n):
    '''
    Function factory which creates a function which converts a number into an n-bit binary vector
    @param n  number of bits to use (or target dimension)
    '''
    def func(x):
        return numpy.array([int(d) for d in format(x, "0{n}b".format(n=4))],
                           dtype=numpy.uint8)

    return func

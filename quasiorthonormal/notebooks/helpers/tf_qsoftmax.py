import tensorflow as tf
def f_qsoftmax(x, basis):
        qx = tf.matmul(tf.constant(basis), x,
                       transpose_b=True)
        return tf.nn.softmax(tf.transpose(qx))

def qsoftmax(basis):
    '''
    Quasiorthogonal softmax metafunction. It returns a quasiorthogonal softmax function for the given basis
    '''

    def func(x):
        qx = tf.matmul(tf.constant(basis), x, transpose_b=True)
        return tf.nn.softmax(tf.transpose(qx))

    return func

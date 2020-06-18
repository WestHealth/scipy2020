import numpy as np
#from scipy.special.softmax as softmax

def softmax(x):
        ex=np.exp(x)
        return ex/np.sum(ex)
        
def f_qsoftmax(x, basis):                                                                           
        qx = np.matmul(np.asarray(basis),x)                                                           
        return softmax(qx)                                                                            
                                                                                                      
                                                                                 

def qsoftmax(basis):
        def func(x):
            qx = np.matmul(np.asarray(basis),x)
            return softmax(qx)
        return func

import numpy as np
from scipy.linalg import toeplitz
from numpy.linalg import eig

def ssa(x, M, method = 'unbiased'):
    '''SSA - driver routine to perform Singular Spectrum Analysis

    Syntax: [E,V,A,R,C]=ssa(x,M); [E,V,A,R,C]=ssa(x,M,method); 
    
    Input:    x - time series 
              M - embedding dimension. 
         method - (optional) method of calculating the covariance matrix: 
                    'unbiased' (N-k weighted) (default) 
                    'biased'   (N-weighted or Yule-Walker)   
                    'BK'       (Broomhead/King type estimate) 
    
    Returns
    -------
    E - eigenfunction (T-EOF) matrix in standard form 
    V - vector containing variances (unnormalized eigenvalues) 
    A - Matrix of principal components 
    R - Matrix of reconstructed components 
    C - Covariance matrix 
    '''

    E, V, C = ssaeig(x, M, method)
    pc(x, E)
    # A = pc(x, E)
    # R = rc(A, E)

    # return E, V, A, R, C

def ssaeig(x, M, method = "unbiased"):
    ''' SSAEIG - starts an SSA of series 'x', for embedding dimension 'M'. 

    Syntax: [E,V,C]=ssaeig(x,M); [E,V,C]=ssaeig(x,M,'BK');   
     
    Input:    x - time series 
              M - embedding dimension. 
         method - (optional) method of calculating the covariance matrix: 
                    'unbiased' (N-k weighted) (default) 
                    'biased'   (N-weighted or Yule-Walker)   
                    'BK'       (Broomhead/King type estimate) 
    
    Output:   E - eigenfunction matrix in standard form 
                  (columns are the eigenvectors, or T-EOFs) 
              V - vector containing variances (unnormalized eigenvalues) 
              C - covariance matrix 
     
    E and V are ordered from large to small. 
    '''

    N = x.shape[0]
    # np.shape return only 1 value in tuple if it's 1 x N array
    try:
        col = x.shape[1]
        if col != 1:
            raise Exception("Vectors only!") # if not 1 x N array
    except IndexError:
        col = 1 # if x.shape[1] is -> 1 x N array

    if M >= N-M+1:
        raise Exception("M, Too big a lag!")     

    # =========================================================

    if method != 'BK':
        c = ac(x, M-1, method) # calculate autocovariance estimates
        C = toeplitz(c) # create Toeplitz matrix (trajectory matrix) 
    else:
        #TODO
        '''
        C = bk(x, M) # Broomhead/King estimate
        '''
    
    # calculate eigenvectors, values of C , L = eigvalues, E = eigvectors
    # note that the eigenvalues are returned as 1-D array in the Numpy case,
    # but 2-D matrix in the MATLAB case. Therefore the call to np.diag is
    # not needed in the Numpy case.
    L, E = eig(C)
    idx = L.argsort()[::-1]  # create sorted eigenvalue vector
    V = L[idx]
    E = E[:,idx] # sort eigenvector matrix 
    
    return E, V, C







def pc(x, E):
    ''' PC - calculates principal components 

    Syntax: [A]=pc(x, E);  

    PC calculates the principal components of the series x 
    from the eigenfunction matrix E (output from SSAEIG).

    Returns:
        A - principal components matrix (N-M+1 x M) 
    '''

    N = x.shape[0]
    # np.shape return only 1 value in tuple if it's 1 x N array
    try:
        col = x.shape[1]
        if col != 1:
            raise Exception("Vectors only!") # if not 1 x N array
    except IndexError:
        col = 1 # if x.shape[1] is null -> 1 x N array


def rc():
    pass

def ac(x, k, method = "unbiased"):
    ''' Calculates the auto-covariance

    Syntax c=ac(x,k);  c=ac(x,k,'biased');

    AC calculates the auto-covariance for series x out to lag k. The  
    result is output in c, which has k+1 elements. The first element 
    is the covariance at lag zero; succeeding elements 1:k+1 are the 
    covariances at lags 1 to k. 
     
    Method can be: - 'biased'   (N-weighted or Yule-Walker)   
                   - 'unbiased' (N-k weighted - this is the default) 
                   - 'BK'       (Broomhead/King type estimate) 
    
    Note that the 'BK' method is of limited use unless you are computing 
    the full covariance matrix - see BK.M.
    '''

    N = x.shape[0]
    try:
        col = x.shape[1]
        if col != 1:
            raise Exception("Vectors only!") # if not 1 x N array
    except IndexError:
        col = 1


    if k > N:
        raise Exception("Too big a lag!")

    x = x - np.mean(x)
    c = np.zeros((k+1))
    
    if method == "unbiased":
        for i in range(k+1):
            c[i] = np.dot(x[0:N-i].T, x[i:N]) / (N-i)
        return c
    
    elif method == "biased":
        #TODO
        '''
        for i=1:k+1 
            c(i)=x(1:N-i+1)'*x(i:N); 
        end 
        c=c./N; 
        '''
        pass

    elif method == "BK":
        #TODO
        '''
        for i=1:k+1 
            c(i)=x(1:N-k)'*x(i:N-k+i-1); 
        end 
        c=c./(N-k); 
        '''
        pass

    else:
        raise Exception('Improper specification of method.') 
            
        
    



    pass

def bk():
    pass

##########################################################################################################

if __name__ == '__main__':
    plt_data = np.array([ -899.,  -899., -1670., -2184., -2441., -2441.,  1156.,  2955.,  -899., -1413.,
                        -1156., -1156., -1156.,  -642.,  -642., -1156.,  -899.,  -128.,   385.,  -385.,
                        -642.,  -642.,   128.,   385.,  2441.,  2955.,  2698.,  2184.,  2441.,  2698.,
                        2441.,  2698.,  4754.,  4754.,  4240.,  4497., 5268.,  5011.,  5525.,  6296.,
                        3983.,  3726.,  4754.,  4240.,  4240.,  5525.,  5011.,  5525.,  5782.,  6553.,
                        7581.,  8609.,  9123.,  7581.,  7581.,  6810.,  5782.,  6039.,  5525.,  6810.,
                        7067.,  5268.,  6296.,  6810.,  6553.,  8866.,  9637.,  8352., 10151., 10151.,
                        10665., 11179.,  7324.,  7838.,  7324.,  3726.,  6039.,  6039.,  8352.,  8095.,
                        8609., 10408.])

    M = 17
    plt_data = plt_data.transpose()
    ssa(plt_data, M)
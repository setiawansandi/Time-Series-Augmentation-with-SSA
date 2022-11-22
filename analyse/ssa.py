import numpy as np

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

    ssaeig(x, M, method)
    # E, V, C = ssaeig(x, M, method)
    # A = pc(x, E)
    # R = rc(A, E)

    # return E, V, A, R, C

def ssaeig(x, M, method = "unbiased"):
    N = x.shape[0]

    # np.shape return only 1 value in tuple if it's 1 x N array
    try:
        col = x.shape[1]
        if col != 1:
            raise Exception("[ERROR] Vectors only!") # if not 1 x N array
    except:
        col = 1 # if null -> 1 x N array

    if M >= N-M+1:
        raise Exception("[ERROR] Too big a lag!")     

    # =========================================================

    if method != 'BK':
        c = ac(x, M-1, method) # TODO
    
    else:
        C = bk(x, M)
    



plt_data = np.array([ -899.,  -899., -1670., -2184., -2441., -2441.,  1156.,  2955.,  -899., -1413.,
                    -1156., -1156., -1156.,  -642.,  -642., -1156.,  -899.,  -128.,   385.,  -385.,
                    -642.,  -642.,   128.,   385.,  2441.,  2955.,  2698.,  2184.,  2441.,  2698.,
                    2441.,  2698.,  4754.,  4754.,  4240.,  4497., 5268.,  5011.,  5525.,  6296.,
                    3983.,  3726.,  4754.,  4240.,  4240.,  5525.,  5011.,  5525.,  5782.,  6553.,
                    7581.,  8609.,  9123.,  7581.,  7581.,  6810.,  5782.,  6039.,  5525.,  6810.,
                    7067.,  5268.,  6296.,  6810.,  6553.,  8866.,  9637.,  8352., 10151., 10151.,
                    10665., 11179.,  7324.,  7838.,  7324.,  3726.,  6039.,  6039.,  8352.,  8095.,
                    8609., 10408.])





def pc():
    pass


def rc():
    pass

def ac(x, k, method = "unbiased"):
    '''
    Syntax c=ac(x,k);  c=ac(x,k,'biased');

    AC calculates the auto-covariance for series x out to lag k. The  
    result is output in c, which has k+1 elements. The first element 
    is the covariance at lag zero; succeeding elements 2:k+1 are the 
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
            raise Exception("[ERROR] Vectors only!") # if not 1 x N array
    except:
        col = 1


    if k > N:
        raise Exception("[ERROR] Too big a lag!")

    x = x - np.mean(x)
    c = np.zeros((k+1))
    
    print(f"N:{N}")
    if method == "unbiased":
        for i in range(k+1):
            c[i] = np.dot(x[0:N-i].T, x[i:N]) / (N-i)
    
    
    
    # print(c)
    # print(c[i])
    # print(f'======== {i} ========')
            
        
    



    pass

def bk():
    pass

M = 17
plt_data = plt_data.transpose()
ssa(plt_data, M)
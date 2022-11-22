
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
    A = pc(x, E)
    R = rc(A, E)

    return E, V, A, R, C

def pc():
    pass

def rc():
    pass

def ssaeig():
    pass
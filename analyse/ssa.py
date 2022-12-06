import numpy as np
from numpy.matlib import repmat
from scipy.linalg import toeplitz
from scipy.signal import lfilter
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
    A = pc(x, E)
    R = rc(A, E)

    return E, V, A, R, C



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
            raise ValueError("Vectors only!") # if not 1 x N array
    except IndexError:
        col = 1 # if x.shape[1] is -> 1 x N array

    if M >= N-M+1:
        raise ValueError("M, Too big a lag!")     

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
    V = -L[idx]
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
            raise ValueError("Vectors only!") # if not 1 x N array
    except IndexError:
        col = 1 # if x.shape[1] is null -> 1 x N array

    x = x - np.mean(x)

    M, c = E.shape
    if M != c: raise ValueError("E is improperly dimensioned")

    A = np.zeros((N-M+1,M))

    for i in range(N-M+1):
        w = x[i:i+M]
        A[i,:] = np.dot(w.T, E)
    
    return A



def rc(A, E):
    '''Calculates the 'reconstructed components'

    Syntax: [R]=rc(A,E);

    This function calculates the 'reconstructed components' using the  
    eigenvectors (E, from ssaeig.m) and principal components (A, from pc.m). 
    R is N x M, where M is the embedding dimension used in ssaeig.m. 
    '''
    
    M, c = E.shape
    ra, ca = A.shape

    if M != c: raise ValueError('E is improperly dimensioned.')
    if ca != M: raise ValueError('A is improperly dimensioned.')
    N = ra+M-1;  # Assumes A has N-M+1 rows.

    R = np.zeros((N,M))
    Z = np.zeros((M-1,M))
    A = np.append(A.T,  Z.T, axis=1)
    A = A.T
    
    # Calculate RCs
    for k in range(M):
        R[:,k] = lfilter(E[:,k], M, A[:,k])
    
    # Adjust first M-1 rows and last M-1 rows
    for i in range(M-1):
        R[i,:] *= (M/(i+1))
        R[N-i-1,:]=R[N-i-1,:]*(M/(i+1));

    return R



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
            raise ValueError("Vectors only!") # if not 1 x N array
    except IndexError:
        col = 1


    if k > N:
        raise ValueError("Too big a lag!")

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
        raise ValueError('Improper specification of method.') 
            


def bk():
    pass



def wcor(x, L):
    ''' 
    Syntax:
        [R] = wcor(x, L)
    '''
    N = x.shape[0]
    K = N - L + 1
    Ls = min(L, K)
    Ks =  max(L, K)

    # w = [1:(Ls-1) repmat(Ls, [1 Ks-Ls+1]) (Ls-1):-1:1]'
    # Compute weights
    val1 = [i for i in range(1,Ls)]
    val2 = repmat(Ls, 1, Ks-Ls+1).flatten()
    val3 = [i for i in range(Ls-1, 0, -1)]
    w = np.hstack((val1, val2, val3)); w=w[:, np.newaxis] # convert to [4x1]

    # Compute w-covariation
    xx = np.multiply(np.sqrt(repmat(w, 1, x.shape[1])), x) # weight matrix of data
    covmat = np.dot(xx.T, xx)        #  cov <- crossprod(sqrt(w) * x);
    # covmat is [ sx1x1 sx1x2 sx1x3...  where x1 is col vector- time series x1
    #             sx2x1 sx2x2 sx2x3...  and so on
    # Convert to correlations

    # Convert to correlations
    Is = 1./np.sqrt(np.diag(covmat))
    Is = Is[:, np.newaxis] # so shape of Is is [n x 1] not [n]
    # diagonals contain the magnitude of each data vector (time series)
    # R = Is * cov * Is';             %  R <- Is * cov * rep(Is, each = nrow(cov));
    # Is*Is' is a col*col matrix containing cross products - except diagonals
    R = np.dot(Is, Is.T) * covmat
    R = abs(R);
    
    return R
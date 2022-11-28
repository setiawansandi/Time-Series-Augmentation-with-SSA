from operator import itemgetter
import numpy as np
from scipy.fftpack import fft, ifft

def aaft(xV, nsur):
    ''' AAFT (Amplitude Adjusted Fourier Transform)

    Syntax: [zV] = aaft(xV, nsur)
    
    For more details see: D. Kugiumtzis, "Surrogate data test for nonlinearity 
                          including monotonic transformations",Phys. Rev. E, 
                          vol. 62, no. 1, 2000.
    
    generates surrogate data for a given time series 'xV' using the AAFT  

    INPUT:     xV - The original time series (column vector)
             nsur - The number of surrogate data to be generated

    OUTPUT:    zV - The CAAFT surrogate data (matrix of 'nsur' columns)
    
    '''

    n = len(xV);

    # The following gives the rank order, ixV
    # p.s.:    The zip(*iterable) idiom reverses the zip process (unzip).
    #          key argument specify which value to sort
    #          return sorted matrix and previous syntax's index
    T1, oxV = zip(*sorted(enumerate(xV), key=itemgetter(1)))
    ixV, T = zip(*sorted(enumerate(T1), key=itemgetter(1)))


    # ====================== AAFT algorithm ======================
    zV = np.zeros((n,nsur));

    for count in range(nsur):
        # Rank ordering white noise with respect to xV 
        rv = np.random.randn(n, 1)
        T, orV = zip(*sorted(enumerate(rv), key=itemgetter(1)))
        yV = np.asarray(orV)[np.asarray(ixV)] # convert tuple to np.array then sort
    
        # Phase randomisation (Fourier Transform): yV -> yftV 
        if n % 2 == 0:
            n2 = n//2
        else:
            n2 = (n-1)//2
        
        yV = yV.flatten() # to 1D array
        tmpV = fft(yV,n=2*n2)
        
    '''
    for count=1:nsur;
        rV = randn(n,1); % Rank ordering white noise with respect to xV 
        [orV,T]=sort(rV);   
        yV = orV(ixV); % Y
    '''

    return -1
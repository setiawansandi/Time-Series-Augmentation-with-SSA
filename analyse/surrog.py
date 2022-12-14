from operator import itemgetter
import numpy as np
from scipy.fftpack import fft, ifft

def aaft(xV, nsur, plot_ok=False):
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
    # T1 holds indices of sorted values
    # ixV tells how to get back original waveform from a sorted list
    # p.s.:    The zip(*iterable) idiom reverses the zip process (unzip).
    #          key argument specify which value to sort
    #          return sorted matrix and previous syntax's index in tuple
    T1, oxV = zip(*sorted(enumerate(xV), key=itemgetter(1)))
    ixV, T = zip(*sorted(enumerate(T1), key=itemgetter(1)))


    # ====================== AAFT algorithm ======================
    zV = np.zeros((n,nsur))

    for count in range(nsur):

        # Rank ordering white noise with respect to xV 
        rv = np.random.randn(n, ) # returns an sz1-by-...-by-szN arr of random number
        T, orV = zip(*sorted(enumerate(rv), key=itemgetter(1)))
        yV = np.asarray(orV)[np.asarray(ixV)] # yV tracks the shape of xV - plot! 
    
        # >>>>> Phase randomisation (Fourier Transform): yV -> yftV 
        if n % 2 == 0:
            n2 = n//2 # even number of samples
        else:
            n2 = (n-1)//2
        
        tmpV = fft(yV,n=2*n2) # FFT the tracking waveform
        magnV = abs(tmpV) # magnitude
        fiV = np.angle(tmpV) # angle
        rfiV = np.random.randn(n2-1, ) * 2 * np.pi # random phase angles only half needed
        nfiV = np.hstack(([0], rfiV, fiV[n2], -np.flipud(rfiV)))

        # New Fourier transformed data with only the phase changed
        tmpV = np.hstack((magnV[0:n2+1].T, np.flipud(magnV[1:n2]).T)).T # so tmpV = magnV?
        tmpV = np.multiply(tmpV, np.exp(nfiV * 1j))

        # Transform back to time domain
        yftV = np.real(ifft(tmpV, n)) # 3-step AAFT

        if plot_ok:
            from utils.plot import Plot
            titles = ['Original data X', 'Random data Y, tracks original', 'Phase randomized version of Y']
            Plot.aaft(xV, yV, yftV, titles=titles)
        # <<<<<

        # Rank ordering xV with respect to yftV
        T2, T = zip(*sorted(enumerate(yftV), key=itemgetter(1)))
        iyftV, T = zip(*sorted(enumerate(T2), key=itemgetter(1)))

        # zV is the AAFT surrogate of xV
        zV[:,count] = np.asarray(oxV)[np.asarray(iyftV)]
        if count == 0: zV = zV.flatten() # flatten if there is only 1 column
    
    return zV

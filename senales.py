import numpy
import scipy
import matplotlib.pyplot as plt

x=numpy.linspace(-1, 1, 1000)
t=numpy.linspace(-3*numpy.pi,3*numpy.pi,1000)
from scipy.signal import chirp, sawtooth, square, gausspulse

plt.figure()
plt.subplot(221)
plt.plot(x,chirp(x,f0=100,t1=0.5,f1=200))
plt.ylim([-2,2])
plt.subplot(222)
plt.plot(x,gausspulse(x,fc=10, bw=0.5))
plt.ylim([-2,2])
plt.subplot(223)
plt.plot(t,sawtooth(t))
plt.ylim([-2,2])
plt.subplot(224)
plt.plot(t,square(t))
plt.ylim([-2,2])
plt.show()

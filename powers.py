import numpy
import scipy
from numpy import floor, sqrt, zeros, rot90, exp2, log2, where, multiply, linspace, ones
from scipy.interpolate import *
import matplotlib.pyplot as plt

def covering(m):
    width=int(floor(0.5*(sqrt(2*m-3)-1)))
    A=zeros((2*width+3,2*width+3))
    for n in range(1+width):
        for k in range(n+1):
            z=2*(n**2+n+1)+k
            A[n+2-k+width,k+1+width]=z
            A[-k+width+1,n+2-k+width]=z+n+1
            A[k-n+width,-k+width+1]=z+2*n+2
            A[k+width+1,k-n+width]=z+3*n+3
    A[width+1,width+1]=1
    return rot90(A.astype(int))

is_power_of_two= lambda x: x==exp2(floor(log2(x)))
is_power_of_four= lambda x: x==4**(floor(log2(x)/2.0))

def powerplot(m):
    values=covering(m)
    locations=where(multiply(is_power_of_two(values), values>0))
    order=values[locations].argsort()

    t=linspace(0,1,locations[0].size)
    tt=linspace(0,1,100*locations[0].size)
    x=InterpolatedUnivariateSpline(t,locations[1][order])
    y=InterpolatedUnivariateSpline(t,-locations[0][order])
    for index in range(locations[0].size):
	plt.text(locations[1][index],-locations[0][index], 
		 str(values[locations[0][index],locations[1][index]]))
    plt.axis('off')
    plt.plot(x(tt),y(tt),'b')

plt.subplot(121); powerplot(exp2(10))
plt.subplot(122); powerplot(exp2(20)); plt.show()

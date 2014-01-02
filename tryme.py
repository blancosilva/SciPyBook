import numpy
from numpy import pi,cos,sin,linspace,zeros,hstack,vstack
import scipy.spatial
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt

parameter=lambda s:linspace(0,1,s)
ellipse = lambda a,b,s:[a*cos(2*pi*parameter(s)), b*sin(2*pi*parameter(s))]
domain = zeros((2,64*4))
domain[0,0:32]=512*parameter(32)-256
domain[1,0:32]=256
domain[0,32:32*2]=512*parameter(32)-256
domain[1,32:32*2]=-256
domain[0,32*2:32*3]=256
domain[1,32*2:32*3]=512*parameter(32)-256
domain[0,32*3:32*4]=-256
domain[1,32*3:32*4]=512*parameter(32)-256
for k in range(16):
        domain=hstack((domain,ellipse(128+16*k,32+16*k,32+2*k)))
	print domain.shape

triangulation=Delaunay(domain.T)
plt.triplot(domain[0],domain[1]); plt.show()


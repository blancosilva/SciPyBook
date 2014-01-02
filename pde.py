import numpy
import scipy
import matplotlib.pyplot as plt
from numpy import pi,cos,sin,hstack,vstack,linspace,where,ones,multiply
from numpy import array, mat, cross, mean, zeros, mgrid
from scipy.special import exp10
from scipy.spatial import Delaunay
from scipy.linalg import norm
from scipy.sparse import dok_matrix
from scipy.sparse.linalg import spsolve
from scipy.interpolate import LinearNDInterpolator

paramtr=lambda s:linspace(0,1,s)
ellipse=lambda a,b,s:[a*cos(2*pi*paramtr(s)), b*sin(2*pi*paramtr(s))]

vertices=ellipse(128,16,48)
for k in range(16):
    vertices=hstack((vertices,ellipse(128+16*k, 16+16*k, 48+2*k)))

horizontal=linspace(-200,200,26)
vertical=linspace(-100,100,16)
vertices=hstack((vertices,vstack((horizontal, 100*ones(26)))))
vertices=hstack((vertices,vstack((horizontal,-100*ones(26)))))
vertices=hstack((vertices,vstack((200*ones(16),vertical))))
vertices=hstack((vertices,vstack((-200*ones(16),vertical))))

inside_vertices=where( multiply(abs(vertices[0])<=200,
    abs(vertices[1])<=100))
vertices=vertices[:,inside_vertices[0]]

triangulation=Delaunay(vertices.T)

index2point=lambda index:triangulation.points[index]
all_centers=index2point(triangulation.vertices).mean(axis=1)
not_in_wing=lambda pt: (pt[0]/128)**2+(pt[1]/16)**2>=1
trngl_set=triangulation.vertices[where(map(not_in_wing, all_centers))]

kappa=lambda pt: exp10(6)*(pt[0]>99.99)
gN=lambda pt:float(pt[0]<=99.99)

points=triangulation.points.shape[0]
stiff_matrix=dok_matrix((points,points))
Robin_matrix=dok_matrix((points,points))
Robin_vector=zeros((points,1))

for triangle in triangulation.vertices:
    helper_matrix=dok_matrix((points,points))
    pt1,pt2,pt3=index2point(triangle)
    area=abs(0.5*cross(pt2-pt1,pt3-pt1))
    coeffs=0.5*vstack((pt2-pt3,pt2-pt1,pt1-pt2))/area
    helper_matrix[triangle,triangle]=array(mat(coeffs)*mat(coeffs).T)
    stiff_matrix=stiff_matrix+helper_matrix

for edge in triangulation.convex_hull:
    helper_matrix=dok_matrix((points,points))
    length=norm(index2point(edge))
    center=mean(index2point(edge),axis=0)
    helper_matrix[edge,edge]=length*kappa(center)*array([[2,1],[1,2]])
    Robin_matrix=Robin_matrix+helper_matrix
    Robin_vector[edge]+=gN(center)*length*0.5*ones((2,1))

solution_vector=spsolve(stiff_matrix+Robin_matrix,Robin_vector)
solution=LinearNDInterpolator(triangulation.points, solution_vector)

X,Y=mgrid[-200:200,-100:100]
#plt.subplot(121); plt.axis('off')
plt.triplot(vertices[0]+200, vertices[1]+100,
	triangles=trngl_set,linewidth=0.3)
#plt.subplot(122)
plt.imshow(solution(-X,Y).T); plt.axis('off')
elpse=ellipse(128,16,48)
#plt.plot(elpse[0]+200,elpse[1]+100,'k-')
plt.show()

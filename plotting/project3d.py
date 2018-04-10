import numpy as np
import cv2 as cv2
import sys as sys
import math as math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

def project3d(maskedImg):
    xres,yres,nColors = maskedImg.shape

    xmid = int(xres/2)
    ymid = int(yres/2)

    xCo = []
    yCo = []
    zCo = []
    colorValue = []

    # xCo = np.zeros((xres,yres),dtype='float')
    # yCo = np.zeros((xres,yres),dtype='float')
    # zCo = np.zeros((xres,yres),dtype='float')

    for i in range (0,xres,7):
        for j in range (0,yres,7):
            xCo.append(i)
            yCo.append(j)

            if maskedImg[i,j,0] == 0:
                zFunc = 0
            else:
                r = math.sqrt((i-xmid)**2+(j-ymid)**2)
                zFunc = -0.46/140*r**2+0.46*140

            zCo.append(zFunc)

            # divide by 256 to normalize
            colorB = maskedImg[i,j,0]/256
            colorG = maskedImg[i,j,1]/256
            colorR = maskedImg[i,j,2]/256

            colorValue.append([colorR,colorG,colorB])


    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_aspect('equal')

    scat = ax.scatter(xCo, yCo, zCo, c=colorValue)

    xCo = np.asarray(xCo,dtype='float')
    yCo = np.asarray(xCo,dtype='float')
    zCo = np.asarray(xCo,dtype='float')

    max_range = np.array([xCo.max()-xCo.min(), yCo.max()-yCo.min(), zCo.max()-zCo.min()]).max()
    Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(xCo.max()+xCo.min())
    Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(yCo.max()+yCo.min())
    Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(zCo.max()+zCo.min())
    # Comment or uncomment following both lines to test the fake bounding box:
    for xb, yb, zb in zip(Xb, Yb, Zb):
        ax.plot([xb], [yb], [zb], 'w')

    plt.grid()
    plt.show()

    sys.exit('MY STOP')

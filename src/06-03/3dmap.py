__author__ = 'amrit'

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 20}

plt.rc('font', **font)
paras={'lines.linewidth': 5,'legend.fontsize': 20, 'axes.labelsize': 30, 'legend.frameon': False,'figure.autolayout': True,'figure.figsize': (16,8)}
plt.rcParams.update(paras)
fig = plt.figure(num=0, figsize=(25, 15))
ax = fig.gca(projection='3d')
X = np.arange(-5, 5, 1)
Y = np.arange(-5, 5, 1)
#X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.arange(-5, 5, 1)
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
#ax.set_zlim(-1.01, 1.01)

ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()
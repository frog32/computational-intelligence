import numpy as np
x = np.arange(6)
y=np.array([0,0,1,2,5,9])
X = np.c_[np.ones(6), x, x**2]
m = np.linalg.lstsq(X,y)[0]

plot(x,y,'.', x, m[0] + m[1] * x + m[2] * x ** 2, 'r')
from numpy import array, c_, tile, zeros
from cvxopt import matrix, solvers

x = array([[0, 1], [2, 1], [2, 2]])
y = array([-1, -1, 1])
k = zeros(3)
Q = array([[1, 0, 0], [0, 1, 0], [0, 0, 0]])
A = c_[tile(-y, (2,1))* x.T, tile(-y.T, (1, 1))]
u = array([-1] * 3).T

sol = solvers.qp(matrix(Q, tc='d'), matrix(k), matrix(A, tc='d'), matrix(u, tc='d'))

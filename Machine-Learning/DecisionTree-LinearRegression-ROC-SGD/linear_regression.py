%matplotlib inline
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy as sc
import pandas as pd
from numpy.linalg import LinAlgError


K = 2
N = 50
m = 0.2

np.random.seed(0)
alpha = 2*np.random.rand(K) - 1
beta = 2*np.random.rand(K) - 1
w = np.arange(1,K+1)
bounds = [-2, 2]

def make_design_matrix(w, om):
    K = len(w)
    N = len(om)
    A = np.empty((N, 2*K+1))
    for i,x in enumerate(om):
        A[i,0] = x
        A[i, 1:(K+1)] = np.sin(w*x)
        A[i, (K+1):(2*K+1)] = np.cos(w*x)
    return A
theta = np.concatenate([[m], alpha, beta])
x_samples = np.linspace(bounds[0], bounds[1], N)
A = make_design_matrix(w, x_samples)
y = np.dot(A, theta)
# Add reasonably large noise
noise_scale = 0.01
noise_range = (max(y)-min(y))*noise_scale
noises = noise_range*np.random.rand(N) - noise_range/2.0
y_noisy = (y + noises).tolist()


tight_samples = np.linspace(bounds[0], bounds[1], 10*N)
A_tight = make_design_matrix(w, tight_samples)
plt.plot(x_samples, y_noisy, 'bo', tight_samples, np.dot(A_tight, theta), 'k')
plt.show()


def safe_inverse(matrix, regularizer = 0.0001):
    try:
        inverse = np.linalg.inv(matrix)
    except LinAlgError:
        inverse = np.linalg.inv(matrix+np.identity(len(matrix))*regularizer)
    return inverse
OM = np.linspace(0.01,5,51)
EE = np.zeros((len(OM),len(OM)))
actual_values = y_noisy
for i,omega1 in enumerate(OM):
    for j,omega2 in enumerate(OM):
        A = make_design_matrix(np.array([omega1, omega2]), x_samples)
        A_t = np.transpose(A)
        estimated_theta = np.dot( np.dot( safe_inverse(np.dot(A_t, A)), A_t ), actual_values )
        estimated_values = np.dot(A, estimated_theta)
        EE[i, j] = sum((actual_values - estimated_values)**2)
min_index = np.unravel_index(EE.argmin(), EE.shape)
best_w = [OM[min_index[0]], OM[min_index[1]]]

# These lines are for plotting purposes
l = min(OM); r = max(OM);
plt.figure(figsize=(10,10))
plt.imshow(np.log(EE), extent=(l,r,l,r), interpolation='nearest', origin='lower')
plt.show()

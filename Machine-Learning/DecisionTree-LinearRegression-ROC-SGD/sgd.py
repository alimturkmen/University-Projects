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

#np.random.seed(0)
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
noise_scale = 0.1
noise_range = (max(y)-min(y))*noise_scale
noises = noise_range*np.random.rand(N) - noise_range/2.0
y_noisy = (y + noises)

# Assume 'x' is scalar!!!
def f(m, alpha, beta, w, x):
    return m*x+np.dot(alpha, np.sin(w*x))+np.dot(beta, np.cos(w*x))

def error_gradient(m, alpha, beta, w, x, y):
    K = len(w)
    x_len = len(x)
    gradient = np.zeros((3*K+1))
    err = 0
    for i, x_i in enumerate(x):
        e_i = y[i] - f(m, alpha, beta, w, x_i)
        err += e_i**2
        factor = -e_i/x_len
        gradient[0] += x_i*factor
        np_sin = np.sin(w*x_i)
        gradient[1:(K+1)] += np_sin*factor
        np_cos = np.cos(w*x_i)
        gradient[(K+1):(2*K+1)] += np_cos*factor
        gradient[(2*K+1):(3*K+1)] += (np.dot(alpha, np_cos*x_i) - np.dot(beta, np_sin*x_i))*factor
    return (gradient, err)

def SGD(x, y, K, batch_scale=2e-1, MAX_EPOCH=1000, learning_rate = 5e-2,
        momentum = 9e-1, decay_rate = 0.95, epsilon = 1e-4):
    N = len(x)
    batch_size = round(batch_scale*N)
    if batch_size == 0: batch_size = 1
    parameters = 2*np.random.rand(3*K + 1) - 1
    grad = np.zeros((3*K+1))
    ERR = []
    w_history = []
    for epoch in range(MAX_EPOCH):
        idx = np.random.choice(N, batch_size, replace=False)
        x_sample = x[idx]
        y_sample = y[idx]
        mom = momentum*grad
        grad, err = error_gradient(parameters[0], parameters[1:(K+1)],
                              parameters[(K+1):(2*K+1)], parameters[(2*K+1):(3*K+1)],
                              x_sample, y_sample)
        grad += mom
        parameters += learning_rate*(-grad)
        ERR.append(err)
        w_history.append(np.copy(parameters[(2*K+1):(3*K+1)]))
        #learning_rate *= decay_rate
        #momentum *= decay_rate
        #if max(grad) < epsilon: break
    return (parameters, grad, ERR, w_history)

parameters, grad_last, ERR, w_history = SGD(x_samples, y_noisy, K)
tight_samples = np.linspace(bounds[0], bounds[1], 10*N)
A_est = make_design_matrix(parameters[(2*K+1):(3*K+1)], tight_samples)

plt.figure(1)
plt.plot(ERR, 'b')

plt.figure(2)
A_tight = make_design_matrix(w, tight_samples)
plt.plot(x_samples, y_noisy, 'bo', tight_samples, np.dot(A_tight, theta), 'k')
plt.plot(x_samples, y_noisy, 'bo', tight_samples, np.dot(A_est, parameters[0:(2*K+1)]), 'r')

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
plt.scatter(x=[w[0] for w in w_history[:-1]], y=[w[1] for w in w_history[:-1]], c='b')
plt.scatter(x=w_history[-1][0], y=w_history[-1][1], c='w', )
plt.show()


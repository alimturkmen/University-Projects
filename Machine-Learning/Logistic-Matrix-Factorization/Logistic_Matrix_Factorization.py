# -*- coding: utf-8 -*-

#%matplotlib inline

import matplotlib as mpl
import matplotlib.pyplot as plt

import numpy as np

from ipywidgets import interact, interactive, fixed
import ipywidgets as widgets
from IPython.display import clear_output, display, HTML
from matplotlib import rc

M = 32
N = 20

Y_full = np.zeros((M,N))
for i in range(M):
    for j in range(N):
        
        # condition = (i+j)%3 == 1
        # condition = j>i
        # condition = ((i+j)%2 == 1) and (j>i)
        # condition = ((i+j)%2 == 1) or (j>i)
        # condition = ((i+j)%2 == 1) != (j>i)
        # condition = (i-j)%4 == 2
        # condition = (i-j)%4 == 2 or (i+2*j)%7 == 0
        # condition = i%3 == 2 or (j%4 == 2)
        condition = i%5 == 2 or ((j+i)%4 == 2)
        
        if condition:
            Y_full[i,j] = 1

plt.imshow(Y_full, cmap='bwr')
plt.show()

Mask = np.random.rand(M, N) < 0.5
Y = Y_full.copy()
Y[Mask==False] = np.nan
plt.imshow(Y, cmap='bwr')
plt.show()

print('Missing(%) : ', np.sum(1-Mask)/(N*M))

def sigmoid(t):
    return 1./(1+np.exp(-t))

def LogisticMF(Y, K, Mask, eta=0.005, nu=0.1, MAX_ITER = 5000, PRINT_PERIOD=500):
    M = Y.shape[0]
    N = Y.shape[1]
    
    W = np.random.randn(M,K)
    H = np.random.randn(K,N)
    
    YM = Y.copy()
    YM[Mask==False] = 0

    
    for epoch in range(MAX_ITER):
        dLh = np.dot(W.T, YM-Mask*sigmoid(np.dot(W,H))) - nu*H
        H = H + eta*dLh
        dLw = np.dot(YM-Mask*sigmoid(np.dot(W,H)),H.T ) - nu*W
        W = W + eta*dLw

        if epoch % PRINT_PERIOD == 0:
            LL = np.sum( (YM*np.log(sigmoid(np.dot(W,H))) +  (Mask-YM)*np.log(1 - sigmoid(np.dot(W,H)))) ) - nu*np.sum(H**2)/2. - nu*np.sum(W**2)/2. 
            print(epoch, LL)
        
    return W,H

W, H = LogisticMF(Y, K=32, Mask=Mask, MAX_ITER = 50000, PRINT_PERIOD=10000)

thr = 0.5

fig=plt.figure(figsize=(12, 6))
plt.subplot(1,5,1)
plt.imshow(Y_full, cmap='bwr', vmin=0, vmax=1)
plt.subplot(1,5,2)
plt.imshow(Y, cmap='bwr', vmin=0, vmax=1)
plt.subplot(1,5,3)
Y_pred = sigmoid(W.dot(H))
plt.imshow(Y_pred, cmap='bwr', vmin=0, vmax=1)
ax = plt.subplot(1,5,4)
Y_rec = Y_pred > thr
plt.imshow(Y_rec, cmap='bwr', vmin=0, vmax=1)
ax2 = plt.subplot(1,5,5)
plt.imshow(Y_full - Y_rec, cmap='PiYG', vmin=-1, vmax=1)
#plt.show()
plt.close(fig)

def change_thr(thr):
    ax.cla()
    Y_rec = Y_pred > thr
    ax.imshow(Y_rec, cmap='bwr', vmin=0, vmax=1)
    ax2.imshow(Y_full - Y_rec, cmap='PiYG', vmin=-1, vmax=1)
    #plt.show()
    display(fig)

# interact(change_thr, thr=(0.0, 1.0,0.01))
change_thr(0.5)

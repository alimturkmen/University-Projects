#!/usr/bin/env python3
# -*- coding: utf-8 -*-

%matplotlib auto
import numpy as np
import matplotlib.pyplot as plt
import random
import math

import torch as tr
import torch.autograd
from torch.autograd import Variable

def sigmoid(t):
    return 1./(1+np.exp(-t))

M = 10 # Use a square matrix of 50x50. You can change it if you wish
original_matrix = np.array([[float((i + j) % 2 == 0) for j in range(M)] for  i in range(M)])


random.seed(10)
def generate_mask(M = 50, mask_scale=0.1):
    mask_count = math.floor(mask_scale*M**2)
    masks = [(m//M, m%M) for m in np.random.choice(M**2, size=mask_count, replace=False)]
    # BELOW CODE CAN SELECT AN INDEX MORE THAN ONCE BY CHANCE!!
    # masks = [(random.randint(0,M-1), random.randint(0,M-1)) for i in range(mask_count)]
    mask = np.ones((M,M))
    for m in masks:
        mask[m] = False
    return mask

mask = generate_mask(M, 0.5)
num_of_obs = np.sum(mask==1)
Y = original_matrix.copy()
Y[mask==False] = np.nan



# Implement SGD here. Add the method signatures for other gradient descents as well. You can add a batch size parameter to merge
# all types of gradient descents into one method.
def sgd(original_matrix, mask, estimation_rank, MAX_ITER=3000, PRINT_PERIOD=None, batch_scale=0.4, eta=0.01, nu=0.1):
    M = original_matrix.shape[0]
    N = original_matrix.shape[1]
    num_of_obs = np.sum(mask==1)
    batch_size = round(batch_scale*N)
    if batch_size == 0: batch_size = 1
    
    W = np.random.randn(M,estimation_rank)
    H = np.random.randn(estimation_rank,N)
    
    YM = original_matrix.copy()
    YM[mask==False] = 0
    
    for epoch in range(MAX_ITER):
        idx = np.random.choice(N, batch_size, replace=False).tolist()
        mask_sample = mask[:,idx]
        H_sample = H[:,idx]
        YM_sample = YM[:,idx]
        
        dLh = np.dot(W.T, YM_sample-mask_sample*sigmoid(np.dot(W,H_sample))) - nu*H_sample
        # dLh = np.dot(W.T, YM-mask*sigmoid(np.dot(W,H))) - nu*H
        dLw = np.dot( YM_sample-mask_sample*sigmoid(np.dot(W,H_sample)),H_sample.T ) - nu*W
        # dLw = np.dot(YM-mask*sigmoid(np.dot(W,H)),H.T ) - nu*W
        H[:,idx] = H_sample + eta*dLh
        W = W + eta*dLw

        if PRINT_PERIOD is not None and epoch % PRINT_PERIOD == 0:
            LL = np.sum( (YM*np.log(sigmoid(np.dot(W,H))) + (mask-YM)*np.log(1 - sigmoid(np.dot(W,H)))) )/num_of_obs
            # - nu*np.sum(H**2)/2.0 - nu*np.sum(W**2)/2.0
            print(epoch, LL)
        
    return W,H

# Compute error for varying estimation ranks from 1 to M
errors = [] # store the error to this list.
YM = Y.copy()
YM[mask==False] = 0
estimation_ranks = range(1, M+1)
for estimation_rank in estimation_ranks:
    W, H = sgd(Y, mask, estimation_rank)
    # Error is - log likelyhood
    errors.append( -np.sum((YM*np.log(sigmoid(np.dot(W,H))) +  (mask-YM)*np.log(1 - sigmoid(np.dot(W,H)))))/num_of_obs )
plt.figure(1)
plt.plot(estimation_ranks, errors)
plt.show()

ITER_M = np.linspace(1000,5000,5)
RANK_M = np.arange(1,M+1)
EE1 = np.zeros((len(ITER_M),len(RANK_M)))
for i,max_iter in enumerate(ITER_M):
    for j,estimation_rank in enumerate(RANK_M):
        W, H = sgd(Y, mask, estimation_rank, MAX_ITER = int(round(max_iter)))
        # Error is - log likelyhood
        EE1[i,j] = -np.sum((YM*np.log(sigmoid(np.dot(W,H))) +  (mask-YM)*np.log(1 - sigmoid(np.dot(W,H)))))/num_of_obs
plt.figure(2)
plt.imshow(EE1, cmap='hot', interpolation='nearest', origin='lower',
           extent=[min(RANK_M),max(RANK_M),min(ITER_M),max(ITER_M)], aspect='auto')
plt.ylabel('Iterations')
plt.xlabel('Approximation Rank')
plt.colorbar()
plt.show()

MASK_M = np.linspace(0.1,1.0,9,endpoint=False)
EE2 = np.zeros((len(MASK_M),len(RANK_M)))
for i,mask_scale in enumerate(MASK_M):
    for j,estimation_rank in enumerate(RANK_M):
        mask = generate_mask(M, mask_scale)
        num_of_obs = np.sum(mask==1)
        Y = original_matrix.copy()
        Y[mask==False] = np.nan
        YM = Y.copy()
        YM[mask==False] = 0
        W, H = sgd(Y, mask, estimation_rank)
        # Error is - log likelyhood
        EE2[i,j] = -np.sum((YM*np.log(sigmoid(np.dot(W,H))) +  (mask-YM)*np.log(1 - sigmoid(np.dot(W,H)))))/num_of_obs
plt.figure(3)
plt.imshow(EE2, cmap='hot', interpolation='nearest', origin='lower',
           extent=[min(RANK_M),max(RANK_M),min(MASK_M),max(MASK_M)], aspect='auto')
plt.ylabel('Mask Scale')
plt.xlabel('Approximation Rank')
plt.colorbar()
plt.show()


mask = generate_mask(M, 0.5)
num_of_obs = np.sum(mask==1)
Y = original_matrix.copy()
Y[mask==False] = np.nan
W, H = sgd(original_matrix=Y, mask=mask, estimation_rank=10, MAX_ITER=3001, PRINT_PERIOD=500, batch_scale=1)
thr = 0.5
fig=plt.figure(figsize=(12, 6))
plt.subplot(1,5,1)
plt.imshow(original_matrix, cmap='bwr', vmin=0, vmax=1)
plt.title('Original Matrix (Full data)')
plt.subplot(1,5,2)
plt.imshow(Y, cmap='bwr', vmin=0, vmax=1)
plt.title('Masked Data')
plt.subplot(1,5,3)
Y_pred = sigmoid(W.dot(H))
plt.imshow(Y_pred, cmap='bwr', vmin=0, vmax=1)
plt.title('Predicted Data (float)')
ax = plt.subplot(1,5,4)
Y_rec = Y_pred > thr
plt.imshow(Y_rec, cmap='bwr', vmin=0, vmax=1)
plt.title('Predicted Data (bool)')
ax2 = plt.subplot(1,5,5)
plt.imshow(original_matrix - Y_rec, cmap='PiYG', vmin=-1, vmax=1)
plt.title('Error')


##########################PYTORCH#################################

def pytorch_sga(original_matrix, mask, estimation_rank, MAX_ITER=3000, PRINT_PERIOD=None, batch_scale=0.4, eta=0.0045, nu=0.1):  
    M = original_matrix.shape[0]
    N = original_matrix.shape[1]
    num_of_obs = np.sum(mask==1)
    batch_size = round(batch_scale*N)
    if batch_size == 0: batch_size = 1
    
    W = Variable( tr.from_numpy(np.random.randn(M,estimation_rank)), requires_grad=True)
    H = Variable( tr.from_numpy(np.random.randn(estimation_rank,N)), requires_grad=True)
    
    YM = original_matrix.copy()
    YM[mask==False] = 0
    YM = Variable ( torch.from_numpy(YM))
    mask = Variable(torch.from_numpy(mask))
    for epoch in range(MAX_ITER):
        idx = np.random.choice(N, batch_size, replace=False).tolist()
        mask_sample = mask[:,idx]
        H_sample = Variable( tr.from_numpy(H[:,idx].data.numpy()), requires_grad=True)
        
        YM_sample = YM[:,idx]
        
        sig = ( tr.sigmoid(tr.matmul(W, H_sample)))
        LL_sample = tr.sum( (YM_sample*tr.log(sig)) + (mask_sample-YM_sample)*tr.log(1-sig))       
        
        LL_sample.backward()
        
        W.data.add_(eta * W.grad.data)
        H[:,idx].data.add_(eta * H_sample.grad.data)
        H_sample.grad.zero_()
        W.grad.zero_()
        
        if PRINT_PERIOD is not None and epoch % PRINT_PERIOD == 0:
            sig = ( tr.sigmoid(tr.matmul(W, H)))
            LL = -tr.sum( (YM*tr.log(sig) + (mask-YM)*tr.log(1 - sig)) )/num_of_obs
            # - nu*np.sum(H**2)/2.0 - nu*np.sum(W**2)/2.0
            print(epoch, LL.data.numpy())
            
    return W.data.numpy(), H.data.numpy()

mask = generate_mask(M, 0.5)
num_of_obs = np.sum(mask==1)
Y = original_matrix.copy()
Y[mask==False] = np.nan

errors = [] # store the error to this list.
YM = Y.copy()
YM[mask==False] = 0
estimation_ranks = range(1, M+1)
for estimation_rank in estimation_ranks:
    W, H = pytorch_sga(Y, mask, estimation_rank)
    errors.append( -np.sum((YM*np.log(sigmoid(np.dot(W,H))) +  (mask-YM)*np.log(1 - sigmoid(np.dot(W,H)))))/num_of_obs )
plt.figure(4)
plt.plot(estimation_ranks, errors)
plt.show()


ITER_M = np.linspace(1000,5000,5)
RANK_M = np.arange(1,M+1)
EE1 = np.zeros((len(ITER_M),len(RANK_M)))
for i,max_iter in enumerate(ITER_M):
    for j,estimation_rank in enumerate(RANK_M):
        W, H = pytorch_sga(Y, mask, estimation_rank, MAX_ITER = int(round(max_iter)))
        EE1[i,j] = -np.sum((YM*np.log(sigmoid(np.dot(W,H))) +  (mask-YM)*np.log(1 - sigmoid(np.dot(W,H)))))/num_of_obs
plt.figure(5)
plt.imshow(EE1, cmap='hot', interpolation='nearest', origin='lower',
           extent=[min(RANK_M),max(RANK_M),min(ITER_M),max(ITER_M)], aspect='auto')
plt.ylabel('Iterations')
plt.xlabel('Approximation Rank')
plt.colorbar()
plt.show()

MASK_M = np.linspace(0.1,1.0,9,endpoint=False)
EE2 = np.zeros((len(MASK_M),len(RANK_M)))
for i,mask_scale in enumerate(MASK_M):
    for j,estimation_rank in enumerate(RANK_M):
        mask = generate_mask(M, mask_scale)
        num_of_obs = np.sum(mask==1)
        Y = original_matrix.copy()
        Y[mask==False] = np.nan
        YM = Y.copy()
        YM[mask==False] = 0
        W, H = pytorch_sga(Y, mask, estimation_rank)
        EE2[i,j] = -np.sum((YM*np.log(sigmoid(np.dot(W,H))) +  (mask-YM)*np.log(1 - sigmoid(np.dot(W,H)))))/num_of_obs
plt.figure(6)
plt.imshow(EE2, cmap='hot', interpolation='nearest', origin='lower',
           extent=[min(RANK_M),max(RANK_M),min(MASK_M),max(MASK_M)], aspect='auto')
plt.ylabel('Mask Scale')
plt.xlabel('Approximation Rank')
plt.colorbar()
plt.show()


mask = generate_mask(M, 0.5)
num_of_obs = np.sum(mask==1)
Y = original_matrix.copy()
Y[mask==False] = np.nan
W, H = pytorch_sga(original_matrix=Y, mask=mask, estimation_rank=10, MAX_ITER=3000, PRINT_PERIOD=500, batch_scale=1)
thr = 0.5
fig=plt.figure(figsize=(12, 6))
plt.subplot(1,5,1)
plt.imshow(original_matrix, cmap='bwr', vmin=0, vmax=1)
plt.title('Original Matrix (Full data)')
plt.subplot(1,5,2)
plt.imshow(Y, cmap='bwr', vmin=0, vmax=1)
plt.title('Masked Data')
plt.subplot(1,5,3)
Y_pred = sigmoid(W.dot(H))
plt.imshow(Y_pred, cmap='bwr', vmin=0, vmax=1)
plt.title('Predicted Data (float)')
ax = plt.subplot(1,5,4)
Y_rec = Y_pred > thr
plt.imshow(Y_rec, cmap='bwr', vmin=0, vmax=1)
plt.title('Predicted Data (bool)')
ax2 = plt.subplot(1,5,5)
plt.imshow(original_matrix - Y_rec, cmap='PiYG', vmin=-1, vmax=1)
plt.title('Error')
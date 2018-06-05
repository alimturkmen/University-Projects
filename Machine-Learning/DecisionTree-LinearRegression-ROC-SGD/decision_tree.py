#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 18:59:38 2018

@author: furkan
"""

import pandas as pd
import scipy as sc
from sklearn.datasets import load_iris
import numpy as np
import math
import matplotlib.pyplot as plt
    

def ent_of_data(data):
    length=len(data)
    _,occurrences=np.unique(data, return_counts=True)
    e=0
    for occ in occurrences:
       p=occ/(length*1.0)
       e+=p*math.log(p,2)
    return -e

def gini(data):
    length=len(data)
    _,occurrences=np.unique(data, return_counts=True)
    g=0
    for occ in occurrences:
       p=occ/(length*1.0)
       g+=p*p
    return 1-g 
    
    

def entropy(X,c,n):
    f=np.zeros(X.shape)
    f[:,0]=X[:,n]
    f[:,1]=c
    f=f[f[:,0].argsort()]
    ent=[]
    gin=[]
    ig=[]
    uf=np.unique(f[:,0])
    boundries=np.convolve(uf,np.array([0.5,0.5]),mode='valid')
    for tau in boundries:
        idx,=np.where(f[:,0]<tau)
        l=len(idx)/(len(c)*1.0)
        idx=idx[-1]  
        L=ent_of_data(f[:,1][:idx+1])*l
        R=ent_of_data(f[:,1][idx+1:])*(1.0-l)
        ent.append(L+R)
        
        L=gini(f[:,1][:idx+1])*l
        R=gini(f[:,1][idx+1:])*(1.0-l)
        gin.append(L+R)
        
        ig.append(ent_of_data(f[:,1])-(L+R))
        
    plt.xlabel('Feature'+str(n))
    plt.ylabel('Impurity')
    plt.plot(boundries,ent,".r")
    plt.plot(boundries,gin,".b")
    plt.plot(boundries,ig,"g")
    plt.legend(["Entropy","Gini","Information Gain"])
    for b in boundries:
        plt.axvline(b,ls=":")
    plt.show()

dataset = load_iris()

def scat_data(X,c):
    X=X[:,0:2]
    num_of_labels=len(np.unique(c))
    for x in range(num_of_labels):
        ss=c==x
        plt.plot(X[ss,0],X[ss,1],"o")
    plt.xlabel('Feature 0')
    plt.ylabel('Feature 1')
    plt.show()


X, c = dataset['data'][:,2:], dataset['target']
scat_data(X,c)
entropy(X,c,0)  
entropy(X,c,1)


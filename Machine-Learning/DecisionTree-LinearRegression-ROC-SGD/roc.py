#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 12:32:34 2018

@author: alim
"""

import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.integrate import quad

plot_number = 1

def gaussian(mu, sigma):
    """
    You can give any variance and mean value.
    """
    s = np.random.normal(mu, sigma, 1000)
    count, bins, ignored = plt.hist(s, 30, normed=True)
    plt.plot(bins,integrand_of_gaussion(bins,sigma,mu) ,
                linewidth=2, color='r')
    return integrand_of_gaussion,bins


def integrand_of_gaussion(bins,sigma,mu):
        return 1/(sigma * np.sqrt(2 * np.pi)) * \
                    np.exp( - (bins - mu)**2 / (2 * sigma**2))                    


def plot_curves_of_gaussians(mu1, v1, mu2, v2):
    global plot_number
    sigma1=math.sqrt(v1)    
    sigma2=math.sqrt(v2)
    plt.figure(plot_number); plot_number += 1
    f0,bins0=gaussian(mu1,sigma1)
    f1,bins1=gaussian(mu2,sigma2)
    plt.show()
    lb = min(bins0)
    ub = max(bins1)
    ts=np.linspace(lb,ub,100)

    fpr=[]
    tpr=[]

    for t in ts:
        v0,_=quad(integrand_of_gaussion,t,math.inf, args=(sigma1,mu1))
        fpr.append(v0)
        v1,_=quad(integrand_of_gaussion,t,math.inf, args=(sigma2,mu2))
        tpr.append(v1)
    
    plt.figure(plot_number); plot_number += 1
    plt.plot(fpr,tpr,"b")
    plt.xlabel('1 - specificity')
    plt.ylabel('Recall')
    plt.show()
    
    tpr.reverse()
    fpr.reverse()
    auc=np.trapz(tpr, fpr)
    print("AUC SCORE for Gaussian distribution: "+str(auc))
    
    
plot_curves_of_gaussians(0,0.1,1,0.5)
    
                    
def triangular(a,c,b):
    s= np.random.triangular(a, c, b, 1000)
    count, bins, ignored = plt.hist(s,30,normed=30)
    x=int(len(bins)/2)
    plt.plot(bins[:x+1],integrand_of_triangular1(bins[:x+1],a,c,b),linewidth=2, color='r')
    plt.plot(bins[x:],integrand_of_triangular2(bins[x:],a,c,b),linewidth=2, color='r')
    return bins

    
def integrand_of_triangular1(x,a,c,b):
        return 2*(x-a)/((b-a)*(c-a)*1.0)
    
    
def integrand_of_triangular2(x,a,c,b):
        return 2*(b-x)/((b-a)*(b-c)*1.0)
    
    
def plot_curves_of_triangulars(a0,b0,a1,b1):    
    global plot_number
    c0=(a0+b0)/2.0
    c1=(a1+b1)/2.0
    plt.figure(plot_number); plot_number += 1
    bins0=triangular(a0,c0,b0)
    bins1=triangular(a1,c1,b1)
    lb = min(bins0)
    ub = max(bins1)
    
    ts=np.linspace(lb,ub,100)
    ub=ts[len(ts)-1]
    
    
    plt.show()
    

    fpr=[]
    tpr=[]

    for t in ts:
        if a0<=t and t<=c0:
            v0_1,_=quad(integrand_of_triangular1,t,c0, args=(a0,c0,b0))
            v0_2,_=quad(integrand_of_triangular2,c0,b0, args=(a0,c0,b0))
            v0=v0_1+v0_2
            fpr.append(v0)
        elif t>c0 and t<=b0:
            v0,_=quad(integrand_of_triangular2,t,b0, args=(a0,c0,b0))
            fpr.append(v0)
            
            
        if a1<=t and t<=c1:
            v1_1,_=quad(integrand_of_triangular1,t,c1, args=(a1,c1,b1))
            v1_2,_=quad(integrand_of_triangular2,c1,b1, args=(a1,c1,b1))
            v1=v1_1+v1_2
            tpr.append(v1)
        elif t>c1 and t<=b1:
            v1,_=quad(integrand_of_triangular2,t,b1, args=(a1,c1,b1))
            tpr.append(v1)
       
    smallest=min(len(fpr),len(tpr))
    
    fpr=fpr[:smallest]
    tpr=tpr[:smallest]
    
    plt.figure(plot_number); plot_number += 1
    plt.plot(fpr,tpr,"b")
    plt.xlabel('1 - specificity')
    plt.ylabel('Recall')
    plt.show()
    
    
    tpr.reverse()
    fpr.reverse()
    auc=np.trapz(tpr, fpr)
    print("AUC SCORE for Symmetric triangular distribution: "+str(auc))
    

plot_curves_of_triangulars(2,5,3,8)
    
    
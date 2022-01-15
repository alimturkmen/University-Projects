"""
EM for Gaussian Mixtures
Alim Türkmen
"""

import numpy as np
import matplotlib.pyplot as plt
import math
import random

def normal_density(x, mu, sigma, d):
    try: 
        sigma_inv = np.linalg.inv(sigma)
    except:
        return -1
    num = np.exp( (-0.5) * np.dot(np.dot((x-mu).T, sigma_inv), (x-mu)) )
    denom = np.sqrt( np.power((2*np.pi), d) * np.linalg.det(sigma))
    return num/denom


class GM():
    def __init__(self):
        self.data = np.load('dataset.npy')
        self.expectation_matrix = np.array([[.0, .0, .0] for x in self.data])
        self.prev_ll = -np.inf
        self.threshold = 1.e-5
        self.class_dict = {0:[], 1:[], 2:[]}
        self.initialize_parameters()
    

    def initialize_parameters(self):
        data = self.data
        data_min_0 = np.min(data[:,0])
        data_max_0 = np.max(data[:,0])
        data_range_0 = data_max_0 - data_min_0

        data_min_1 = np.min(data[:,1])
        data_max_1 = np.max(data[:,1])
        data_range_1 = data_max_1 - data_min_1
        
        mean_dict = {}

        for i in range(3):
            feat_0 = data_min_0 + data_range_0 * random.random()
            feat_1 = data_min_1 + data_range_1 * random.random()
            mean_dict[i] = np.array([feat_0, feat_1])
            
        covar_dict = {k:np.array([[1, 0], [0, 1]]) for k in range(3)}

        coeff_dict = {0:0.34, 1:0.33, 2:0.33}

        self.mean_dict = mean_dict
        self.covar_dict = covar_dict
        self.coeff_dict = coeff_dict


    def log_likelihood(self):
        log_likelihood = 0
        for x in self.data:
            log_sum = 0
            for k in self.coeff_dict:
                mu_k = self.mean_dict[k]
                covar_k = self.covar_dict[k]
                coeff_k = self.coeff_dict[k]
                d = 2
                nd = normal_density(x, mu_k, covar_k, d)
                if nd == -1 : 
                    self.initialize_parameters()
                    #print("\nParameters are reinitialized due to singularity.")
                    self.log_likelihood()
                log_sum += coeff_k * nd
            log_sum = 1 if log_sum <= 0 else log_sum
            log_likelihood += math.log(log_sum)
        return log_likelihood


    def E_step(self):
        for i, x in enumerate(self.data):
            sum_rx = 0
            rx = []
            for k in self.coeff_dict:
                mu_k = self.mean_dict[k]
                covar_k = self.covar_dict[k]
                coeff_k = self.coeff_dict[k]
                d = 2
                rx_k = coeff_k * normal_density(x, mu_k, covar_k, d)
                rx.append(rx_k)
                sum_rx += rx_k
            for j in range(3):
                self.expectation_matrix[i,j] = (rx[j] / sum_rx)


    def update_coeffs(self):
        m_dict = {}
        m_sum = 0
        for k in self.coeff_dict:
            m_k = np.sum(self.expectation_matrix[:,k])
            m_dict[k] = m_k
            m_sum += m_k

        for k in self.coeff_dict:
            self.coeff_dict[k] = m_dict[k] / m_sum

        self.m_dict = m_dict


    def update_means(self):
        mu_dict = {k:np.array([.0, .0]) for k in self.coeff_dict}
        for i, x in enumerate(self.data):
            for k in self.coeff_dict:
                mu_dict[k] += (self.expectation_matrix[i][k] * x) / self.m_dict[k]

        self.mean_dict = mu_dict


    def update_covars(self):
        sigma_dict = {k:np.array([[.0, .0], [.0, .0]]) for k in self.coeff_dict}
        for i, x in enumerate(self.data):
            for k in self.coeff_dict:
                x_mu_k = (x - self.mean_dict[k]).reshape(1, 2)
                sigma_x_k = self.expectation_matrix[i][k] * np.dot(x_mu_k.T, x_mu_k) / self.m_dict[k]
                sigma_dict[k] += sigma_x_k

        self.covar_dict = sigma_dict


    def M_step(self):
        self.update_coeffs()
        self.update_means()
        self.update_covars()


    def is_converged(self):
        cur_ll = self.log_likelihood()
        ll_dif = cur_ll - self.prev_ll
        if (ll_dif > 0) and ll_dif < self.threshold :
            return True
        else:
            self.prev_ll = cur_ll
            return False
    

    def assing_classes(self):
        
        for i, x in enumerate(self.data):
            clss = np.argmax(self.expectation_matrix[i,:])
            self.class_dict[clss].append(x)


    def plot_points(self):
        colors = ['b', 'g', 'r']
        for clss in self.class_dict:
            for x in self.class_dict[clss]:
                plt.scatter(x[0], x[1], color=colors[clss], alpha=0.3)
        
        for k in self.mean_dict:
            mean_k = self.mean_dict[k].round(3)
            covar_k = self.covar_dict[k].round(3)
            coeff_k = self.coeff_dict[k].round(3)
            txt = "Mean:\n{}\nCovariance:\n{}\nCoeff:{}".format(mean_k, covar_k, coeff_k)
            plt.text(mean_k[0]-1.5, mean_k[1]-1, txt, size=10)
        plt.show()


def EM():
    gm = GM()
    ll_init = gm.log_likelihood()
    print(f"Initial log-likelihood: {ll_init}")
    iter = 1
    ll_prev = 0

    while not gm.is_converged():
        gm.E_step()
        gm.M_step()
        ll = gm.log_likelihood()
        ll_dif = ll-ll_prev
        ll_prev = ll
        iter += 1
        print(f"Iteration:{iter}\tLog-likelihood:{ll}\tDifference:{ll_dif}", end='\r')
        if np.isnan(ll):
            iter = 1
            gm.initialize_parameters()
            print("\nEncountered overlow, parameters are reinitialized.")

    print()
    return ll, gm


def run(trial_n=5):
    optimal_ll = -np.inf
    optimal_gm = None
    opt_trial = 0
    for n in range(1, trial_n+1):
        print(f"Trial:{n}")
        ll, gm = EM()
        if ll > optimal_ll:
            optimal_ll = ll
            optimal_gm = gm
            opt_trial = n
    print(f"Chose the one with maximum log-likelihood: Trial {opt_trial}")
    optimal_gm.assing_classes()
    optimal_gm.plot_points()


run()
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import math

mu1 = 1
mu2 = -1
var = 1
sigma = math.sqrt(var)
lambda_s, lambda_r = 4, 1
coeff = (lambda_s-lambda_r) / lambda_s
p_omega= 0.5

x = np.linspace(mu2 - 3*sigma, mu1 + 3*sigma, 100)

y1 = stats.norm.pdf(x, mu1, sigma)*p_omega
y2 = stats.norm.pdf(x, mu2, sigma)*p_omega
y3 = (y1+y2)*coeff

r1, r2, r3 = [], [], []
for i in range(len(x)):
    if y1[i] > y2[i] and y1[i] > y3[i] : r1.append(x[i])
    elif y2[i] > y3[i]: r2.append(x[i])
    else: r3.append(x[i])

r1_line = np.full((len(r1), ), 0.25)  
r2_line = np.full((len(r2), ), 0.25) 
r3_line = np.full((len(r3), ), 0.25)                         

plt.plot(x, y1, color='r', label='g1')
plt.plot(r1, r1_line, 'r-')
plt.text(r1[int(len(r1)/3)], 0.24, 'Region 1')
plt.plot(x, y2, color='b', label='g2')
plt.plot(r2, r2_line, 'b-')
plt.text(r2[int(len(r2)/3)], 0.24, 'Region 2')
plt.plot(x, y3, color='g', label='g3')
plt.plot(r3, r3_line, 'g-')
plt.text(r3[0], 0.24, 'Region 3')
plt.legend()

plt.show()
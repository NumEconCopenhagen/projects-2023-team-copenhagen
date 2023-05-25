import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from scipy.optimize import minimize

class Problem2:
    def calculate_profit(kappa,eta,w):
        ell = (((1 - eta) * kappa) / w) ** (1 / eta)
        price = kappa * ell ** (-eta)
        profit = price * ell - w * ell
        return profit
    
    def calculate_profit(kappa,eta,iota,w,ell,t):
        ell = (((1 - eta) * kappa) / w) ** (1 / eta)
        adjustment_cost = iota 
        price = kappa * ell ** (-eta)
        profit = price * ell - w * ell - adjustment_cost
        return ell, profit

    def calculate_ex_post_value(shock_series,T,calculate_profit):
        ell_prev = 0.0
        ex_post_value = 0.0

        for t in range(1,T+1):
            kappa = np.exp(shock_series[t-1])
            ell, profit = calculate_profit(kappa, ell_prev, t-1)
            ex_post_value += R ** (-(t-1)) * profit
            ell_prev = ell

        return ex_post_value
    


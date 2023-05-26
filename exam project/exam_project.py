import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from scipy.optimize import minimize

class ExAnteValueCalculator:
    def __init__(self, eta, w, rho, iota, sigma_epsilon, R, T, K):
        self.eta = eta
        self.w = w
        self.rho = rho
        self.iota = iota
        self.sigma_epsilon = sigma_epsilon
        self.R = R
        self.T = T
        self.K = K
    
    def calculate_profit_b(self, kappa, ell, t):
        ell = (((1 - self.eta) * kappa) / self.w) ** (1 / self.eta)
        adjustment_cost = self.iota
        price = kappa * ell ** (-self.eta)
        profit = price * ell - self.w * ell - adjustment_cost
        return ell, profit

    def calculate_ex_post_value(self, shock_series):
        ell_prev = 0.0
        ex_post_value = 0.0

        for t in range(1, self.T + 1):
            kappa = np.exp(shock_series[t - 1])
            ell, profit = self.calculate_profit_b(kappa, ell_prev, t - 1)
            ex_post_value += self.R ** (-(t - 1)) * profit
            ell_prev = ell

        return ex_post_value

    def calculate_ex_ante_value(self):
        ex_ante_values = []

        for k in range(self.K):
            shock_series = np.random.uniform(-0.5 * self.sigma_epsilon ** 2, self.sigma_epsilon, self.T)
            ex_post_value = self.calculate_ex_post_value(shock_series)
            ex_ante_values.append(ex_post_value)

        ex_ante_value = np.mean(ex_ante_values)
        return ex_ante_value


class ExAnteValueCalculator_a:
    def __init__(self, eta, w, rho, iota, sigma_epsilon, R, T, K, Delta):
        self.eta = eta
        self.w = w
        self.rho = rho
        self.iota = iota
        self.sigma_epsilon = sigma_epsilon
        self.R = R
        self.T = T
        self.K = K
        self.Delta = Delta

    def calculate_profit_c(self, kappa, ell_prev, t):
        ell_ast = (((1 - self.eta) * kappa) / self.w) ** (1 / self.eta)
        adjustment_cost = self.iota * (abs(ell_prev - ell_ast) > self.Delta)
        price = kappa * ell_ast ** (-self.eta)
        profit = price * ell_ast - self.w * ell_ast - adjustment_cost
        return ell_ast, profit

    def calculate_ex_post_value_b(self, shock_series):
        ell_prev = 0.0
        ex_post_value = 0.0

        for t in range(self.T):
            kappa = np.exp(shock_series[t])
            ell, profit = self.calculate_profit_c(kappa, ell_prev, t)
            ex_post_value += self.R ** (-t) * profit
            ell_prev = ell

        return ex_post_value

    def calculate_ex_ante_value(self):
        ex_ante_values = []

        for k in range(self.K):
            shock_series = np.random.uniform(-0.5 * self.sigma_epsilon ** 2, self.sigma_epsilon, self.T)
            ex_post_value = self.calculate_ex_post_value_b(shock_series)
            ex_ante_values.append(ex_post_value)

        ex_ante_value = np.mean(ex_ante_values)
        return ex_ante_value


class ExAnteValueCalculator_b:
    def __init__(self, eta, w, rho, iota, sigma_epsilon, R, T, K):
        self.eta = eta
        self.w = w
        self.rho = rho
        self.iota = iota
        self.sigma_epsilon = sigma_epsilon
        self.R = R
        self.T = T
        self.K = K

    def calculate_profit_d(self, kappa, ell_prev, t, Delta):
        ell_ast = (((1 - self.eta) * kappa) / self.w) ** (1 / self.eta)
        adjustment_cost = self.iota * (abs(ell_prev - ell_ast) > Delta)
        price = kappa * ell_ast ** (-self.eta)
        profit = price * ell_ast - self.w * ell_ast - adjustment_cost
        return ell_ast, profit

    def calculate_ex_post_value_c(self, shock_series, Delta):
        ell_prev = 0.0
        ex_post_value = 0.0

        for t in range(self.T):
            kappa = np.exp(shock_series[t])
            ell, profit = self.calculate_profit_d(kappa, ell_prev, t, Delta)
            ex_post_value += self.R ** (-t) * profit
            ell_prev = ell

        return ex_post_value

    def find_optimal_delta(self, delta_values):
        ex_ante_values = []

        for delta in delta_values:
            ex_ante_sum = 0
            for k in range(self.K):
                shock_series = np.random.uniform(-0.5 * self.sigma_epsilon ** 2, self.sigma_epsilon, self.T)
                ex_post_value = self.calculate_ex_post_value_c(shock_series, delta)
                ex_ante_sum += ex_post_value
            ex_ante_value = ex_ante_sum / self.K
            ex_ante_values.append(ex_ante_value)

        optimal_delta = delta_values[np.argmax(ex_ante_values)]
        max_ex_ante_value = np.max(ex_ante_values)

        return optimal_delta, max_ex_ante_value, ex_ante_values

    def plot_ex_ante_values(self, delta_values, ex_ante_values):
        plt.plot(delta_values, ex_ante_values)
        plt.xlabel("Delta")
        plt.ylabel("Ex Ante Value (H)")
        plt.title("Ex Ante Value (H) vs. Delta")
        plt.show()

import numpy as np

class ExAnteValueCalculator_c:
    def __init__(self, eta, rho, iota, sigma_epsilon, R, T, K):
        self.eta = eta
        self.rho = rho
        self.iota = iota
        self.sigma_epsilon = sigma_epsilon
        self.R = R
        self.T = T
        self.K = K

    def calculate_wage(self, prev_profit):
        w = 1.0 + 0.05 * np.sign(prev_profit)
        return w

    def calculate_profit_e(self, kappa, ell_prev, t, prev_profit):
        w = self.calculate_wage(prev_profit)
        ell_ast = (((1 - self.eta) * kappa) / w) ** (1 / self.eta)
        adjustment_cost = self.iota * (abs(ell_prev - ell_ast) > 0)
        price = kappa * ell_ast ** (-self.eta)
        profit = price * ell_ast - w * ell_ast - adjustment_cost
        return ell_ast, profit, w

    def calculate_ex_ante_value_b(self, delta):
        ex_ante_sum = 0.0

        for k in range(self.K):
            ell_prev = 0.0
            ex_post_value = 0.0
            ex_ante_value = 0.0
            prev_profit = 0.0

            shock_series = np.random.uniform(-0.5 * self.sigma_epsilon ** 2, self.sigma_epsilon, self.T)

            for t in range(self.T):
                kappa = np.exp(shock_series[t])
                ell, profit, wage = self.calculate_profit_e(kappa, ell_prev, t, prev_profit)
                ex_post_value += self.R ** (-t) * profit
                ex_ante_value += self.R ** (-t) * profit
                ell_prev = ell
                prev_profit = profit

            ex_ante_sum += ex_ante_value

        ex_ante_value = ex_ante_sum / self.K
        return ex_ante_value

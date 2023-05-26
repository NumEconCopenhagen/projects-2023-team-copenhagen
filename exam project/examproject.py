import numpy as np

from scipy.optimize import minimize
import matplotlib.pyplot as plt

class GriewankOptimizer:
    def __init__(self, bounds, tau, K_under, K):
        self.bounds = bounds
        self.tau = tau
        self.K_under = K_under
        self.K = K
    
    def griewank(self, x):
        if isinstance(x, float):
            return self.griewank_([x])
        return self.griewank_(x)

    def griewank_(self, x):
        x1 = x[0]
        x2 = 0 if len(x) < 2 else x[1]  # Handle the case when len(x) < 2
        A = x1**2 / 4000 + x2**2 / 4000
        B = np.cos(x1 / np.sqrt(1)) * np.cos(x2 / np.sqrt(2))
        return A - B + 1

    def refined_global_optimizer(self):
        np.random.seed(100)
        # Initialize the optimal solution.
        a_star = None
        # Initialize a list to store the effective initial guesses.
        initial_guesses = []
        # Initialize a_k0 outside of the if statement
        a_k0 = None
        # Iterate over the iterations.
        for k in range(self.K):
            # Draw a random point.
            a_k = np.random.uniform(self.bounds[0], self.bounds[1])
            # If this is the first iteration, or if the current point is better than the
            # previous best point, set it as the new best point.
            if k == 0 or self.griewank(a_k) < self.griewank(a_star):
                a_star = a_k
            # If this is not the first iteration, calculate the probability of moving
            # towards the current best point.
            if k > self.K_under:
                P_k = 0.50 * (2 / (1 + np.exp((k - self.K_under) / 100)))
                # If the probability is greater than 0, move towards the current best point.
                if P_k > 0:
                    a_k0 = P_k * a_k + (1 - P_k) * a_star
                    initial_guesses.append(a_k0)
            # Run the optimizer with the current point as the initial guess.
            if a_k0 is not None:
                a_k_star = self.optimizer(a_k0)  # step.E
                # If the new point is better than the previous best point, set it as the new
                # best point.
                if self.griewank(a_k_star) < self.griewank(a_star):
                    a_star = a_k_star
            # If the new point is within the tolerance, return it.
            if self.griewank(a_star) < self.tau:
                return a_star, initial_guesses
        # Return the best point found.
        return a_star, initial_guesses

    def optimizer(self, x0):
        # Placeholder optimization algorithm, replace with your chosen optimizer
        res = minimize(self.griewank, x0, method='BFGS', tol=self.tau)
        return res.x




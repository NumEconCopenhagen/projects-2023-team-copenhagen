import numpy as np
import matplotlib.pyplot as plt
from types import SimpleNamespace
from scipy import optimize

G = 1

def C(kappa, tau, wage, L):
    """Calculates consumption given the labor supply"""
    
    tax_wage = (1 - tau) * wage
    
    return kappa + (tax_wage * L)

def utility_worker(alpha, C, G, sigma, rho, nu, L, epsilon):
    """Calculates the new utility based on the long formula"""
    
    positive = ((alpha * C**(sigma - 1 / sigma) + (1 - alpha) * G**(sigma - 1 / sigma))**(sigma / (1 - sigma)))**(1 - rho) - 1 / (1 - rho)
    
    negative = nu * (L**(1 + epsilon) / 1 + epsilon)
    
    return positive - negative

def final_utility(alpha, G, sigma, rho, nu, L, epsilon, kappa, tau, wage):
    """This is the final version for the utility function with C applied"""
   
    c = C(kappa, tau, wage, L)
    return utility_worker(alpha, c, G, sigma, rho, nu, L, epsilon)


def optimize_L(alpha, sigma, rho, nu, epsilon, kappa, tau, wage):
    """Finds the optimal labor supply given the parameters"""

    obj = lambda L: -final_utility(alpha, G, sigma, rho, nu, L, epsilon, kappa, tau, wage)

    sol = optimize.minimize_scalar(obj, bounds=(0, 24), method='bounded')
    return sol.x


def new_G(tau, wage, L):
    """New formula for gov consumption"""
    
    return tau * wage * L

def solve_G(alpha, sigma, rho, nu, epsilon, kappa, tau, wage):
    """Solve for the government spending given the parameters"""
    # Find the optimal labor supply
    L_solve = optimize_L(alpha, sigma, rho, nu, epsilon, kappa, tau, wage)
    
    # Calculate the optimal government spending
    G_solve = new_G(tau, wage, L_solve)
    
    return G_solve

def optimal_tax(alpha, sigma, rho, nu, epsilon, kappa, wage):

    obj = lambda tau: -final_utility(alpha, solve_G(alpha, sigma, rho, nu, epsilon, kappa, tau, wage), sigma, rho, nu, optimize_L(alpha, sigma, rho, nu, epsilon, kappa, tau, wage), epsilon, kappa, tau, wage)
    sol = optimize.minimize_scalar(obj, bounds=(0,1), method='bounded')

    return sol.x

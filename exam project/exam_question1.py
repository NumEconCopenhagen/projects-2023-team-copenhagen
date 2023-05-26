import numpy as np
import matplotlib.pyplot as plt
from types import SimpleNamespace
from scipy import optimize

def private_consumption(kappa,tau,wage,L):
    """Calculates comsuption that subjects the labor supply"""

    tax_wage = (1-tau)*wage
    return kappa+(tax_wage*L)


def utility_worker(C,L,G,alpha,nu):
    """Function that return the utility given the otimized values of L"""

    positive = np.log(C**alpha*G**(1-alpha))
    negative = (nu*((L**2)/2))

    return positive-negative


def value_of_choice(L,G,alpha,nu,kappa,tau,wage):
    """Calculate implied utility given the values of c and l"""

    c = private_consumption(kappa,tau,wage,L)
    return utility_worker(c,L,G,alpha,nu)


def optimal_labor_supply(alpha,nu,kappa,tau,wage):
    """Finds the optimal labor supply given the parameters"""
    
    obj = lambda L: -value_of_choice(L, 1, alpha, nu, kappa, tau, wage) #1 because G doesnt affect L
    sol = optimize.minimize_scalar(obj, bounds=(0, 24), method='bounded')
    
    return sol.x

def expected_L(kappa,alpha,nu,tax_wage):
    return (-kappa+(kappa**2 +4*(alpha/nu)*tax_wage**2)**(1/2))/(2*tax_wage)

def gov_endogenous(alpha,nu,kappa,tau,wage):
    """This function shows the gov consumption when it chooses the tax rate"""
    
    L = optimal_labor_supply(alpha,nu,kappa,tau,wage)
    return tau*wage*L

def optimal_tau(alpha,nu,kappa,wage):
    """Returns the optimal value of tau that maximizes the return of value_of_choice function"""
    obj = lambda tau: -value_of_choice(optimal_labor_supply(alpha,nu,kappa,tau,wage),
                                       gov_endogenous(alpha,nu,kappa,tau,wage), alpha, nu, kappa, tau, wage)
    
    sol = optimize.minimize_scalar(obj, bounds=(0, 1), method='bounded')
    
    return sol.x

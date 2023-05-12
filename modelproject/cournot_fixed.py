import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from types import SimpleNamespace
from scipy import optimize
import math

class Firm1:

    def __init__(self):

        """ Model that gives the maximize output for the case of the Firm 1 in the duopoly market
        The model just works for one period and the output of the Firm 2 is already given
        We assume a fixed cost that is present no matter what is the output
        We also assume that both firms sell a homogeneous good 
        The Marginal Cost is going to be 1
        
        c: Marginal Cost
        K: Fixed cost
        P: inverse demand
        q2: Output of firm 2
        a: itercept of the inverse demand (fixed parameter)
        
        """
        #create namespaces to store values
        par = self.par = SimpleNamespace()
        sol = self.sol = SimpleNamespace()

        #create the variables that are fixed
        par.K = 12
        par.c = 1
        par.q2 = 6 #Firm 2 produces this quantity no matter what
        par.P = 13 #fixed compnent in inverse demand

        self.q1 = np.nan

    def profit(self,q1):
        """based on the utility func that is total revenues - toal cost """

        par = self.par
        

        #total revenue
        rev_tot = (par.P-par.q2-q1)*q1
        #total cost
        cost_tot = (par.c*q1)-par.K
        #total profit
        profit_tot = rev_tot-cost_tot
        
        return profit_tot
    
    def solve_q1(self):
        """solve for the q1 that max the utility"""

        sol = self.sol
        
        def u(x):
            return -self.profit(q1=x)
        
        #create bounds equal or larger than 0 because is impossible to produce negative quantities
        bounds = (0,13)
        
        sol = optimize.minimize_scalar(lambda q1: u(q1),bounds=bounds)
        
        self.q1 = sol.x
        self.u = self.profit(self.q1)

        
        print(f'The optimal output for Fimr 1 is: {self.q1:.2f} units')

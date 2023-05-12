import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from types import SimpleNamespace
from scipy import optimize
import math

class Merge:

    def __init__(self):
        """Class that will help to obtain the optimal output for 
        both firms and thus it will yield the Nash Equilibrium
        The parameters are the same as in the previous class just with 
        the difference that here q2 is not given"""

         #create namespaces to store values
        par = self.par = SimpleNamespace()
        sol = self.sol = SimpleNamespace()

        #create the variables that are fixed
        par.K = 12 #fixed cost
        par.c1 = 2  #marginal cost firm 1
        par.c2 = 4 #marginal cost firm 2

        par.P = 13 #fixed compnent in inverse demand

        self.q1 = np.nan
        self.q2 = np.nan
        
        self.Q = np.nan

        #to obtain the surplus
        self.monopoly = np.nan
        self.consumers = np.nan
        self.total_surplus = np.nan

    def unique_profit(self,Q):
        """Function that will give the unique profit for the new merged firm"""

        par = self.par

        rev = (par.P-Q)*Q
        cost = (par.c1*Q)-par.K #we suppose that the new cost is based on the most efficient firm
        profit = rev-cost
        return profit
        
    def solve_Q(self):
        """Function that solves for the otimal quantity of the new monopoly"""
        sol = self.sol
        
        def objective(x):
            return -self.unique_profit(Q=x)
        
        bounds = (0,13)

        cons1 = lambda x: 13-x[0] #this constraint means that if the firm satisfies all the demand is because they sell at 0 price the good
        constraint = ({'type': 'ineq','fun': cons1})

        guess = 6

        sol = optimize.minimize_scalar(objective,guess,bounds=bounds)
            
        self.Q = sol.x

        self.objective = self.unique_profit(Q=self.Q)

        print(f'The optimal output for the monopoly is {self.Q:.2f}')

    def surplus(self):
        """Function that outputs the surplus of the monopoly, the consumers and the total"""

        sol = self.sol
        par = self.par

        price = par.P-self.Q

        self.monopoly = price*self.Q-par.c1*self.Q

        self.consumers = (par.P-price)*self.Q/2

        self.total_surplus = self.monopoly + self.consumers

        print(f'The total surplus is {self.total_surplus:.2f}, \
              the surplus for the mopoly is {self.monopoly:.2f} and \
              the surplus of the consumers is {self.consumers:.2f}')
        


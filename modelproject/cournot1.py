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
        


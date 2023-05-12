import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from types import SimpleNamespace
from scipy import optimize
import math

class Nash_Eq:

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
        par.c = 1  #marginal cost 
        par.P = 13 #fixed compnent in inverse demand

        self.q1 = np.nan
        self.q2 = np.nan

        #surplus for the firms and the consumers, at the end total surplus
        self.firm1_s = np.nan
        self.firm2_s = np.nan
        self.consumers = np.nan
        self.total_surplus = np.nan

    def total_profit(self,q1,q2):

        par = self.par

        #total revenue
        rev_tot1 = (par.P-q2-q1)*q1
        rev_tot2 = (par.P-q2-q1)*q2
        
        #total cost
        cost_tot1 = (par.c*q1)-par.K
        cost_tot2 = (par.c*q2)-par.K
        
        #total profit
        profit_tot1 = rev_tot1-cost_tot1
        profit_tot2 = rev_tot2-cost_tot2
        
        return profit_tot1, profit_tot2
    
    def objective(self,x):
        # set the values for the q based on the x of the optimize
        q1 = x[0]
        q2 = x[1]

        #get the sum of both profits
        return -(self.total_profit(q1,q2)[0]+self.total_profit(q1,q2)[1])
        
    def solve_q1_q2(self):

        par = self.par
        sol = self.sol

        #define the bounds
        bounds = [(0,13),(0,13)]

        #make a guess
        guess = [4,4]

        #for the method 'L-BFGS-B' we need to indicate the max num of iterations and also we just want to show the values that's why the False in disp
        options = {'maxiter': 100, 'disp': False}

        sol = optimize.minimize(self.objective,guess,method='L-BFGS-B',bounds=bounds,options=options)

        self.q1 = sol.x[0]
        self.q2 = sol.x[1]

        self.objective = -sol.fun #give the objective function the maximum value obtain by the optimize function

        print(f'The optimal output for Fimr 1 is: {self.q1:.2f} units.')
        print(f'The optimal output for Fimr 2 is: {self.q2:.2f} units')

    def surplus(self):
        """Function that outputs the surplus of the monopoly, the consumers and the total"""

        sol = self.sol
        par = self.par

        price = par.P-(self.q1+self.q2)

        self.firm1_s = price*self.q1-par.c*self.q1
        self.firm2_s = price*self.q2-par.c*self.q2

        self.consumers = (par.P-price)*(self.q1+self.q2)/2

        self.total_surplus = (self.firm1_s+self.firm2_s) + self.consumers

        print(f'The total surplus is {self.total_surplus:.2f}, \
              the surplus for the Firm 1 is {self.firm1_s:.2f} and for the Firm 2 is {self.firm2_s:.2f}\
              the surplus of the consumers is {self.consumers:.2f}')
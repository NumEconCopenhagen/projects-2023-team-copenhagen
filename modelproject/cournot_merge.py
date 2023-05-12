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
        
class Mergegraph:
    
    def __init__(self, b_val=1, c_val=1, k=12):
        self.b_val = b_val
        self.c_val = c_val
        self.k = k
        self.intersection_x = (2*(self.c_val+self.k - self.c_val)) / (3 * self.b_val)
        self.intersection_y = self.c_val+self.k-self.b_val*self.intersection_x
        self.x1_vec = self.intersection_x/2
        self.x2_vec = self.intersection_x/2
        self.p = self.c_val+self.k-self.b_val*(self.x1_vec+self.x2_vec)
        self.p_ = (self.c_val+self.k+2*self.c_val)/3

    def plot(self):
        x1_ = np.linspace(0,13,100)
        x2_ = np.linspace(0,13,100)
        x_true = x1_+x2_
        p_line = self.c_val+self.k-self.b_val*x_true
        mask = x_true < 13 # create a boolean mask based on the condition
        x_true = x_true[mask] # apply the mask to filter out the values that don't satisfy the condition
        p_line = self.c_val + self.k - self.b_val * x_true
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.plot(x_true, p_line, label='p')
        ax.axhline(y=self.p_, color='r', linestyle='--', label='p_')
        ax.scatter(0, self.c_val+self.k, s=50, marker='o', color='black')
        ax.text(0.2, self.c_val+self.k+0.2, 'E', fontsize=15)
        ax.scatter(self.intersection_x, self.intersection_y, s=50, marker='o', color='black')
        ax.text(self.intersection_x , self.intersection_y + 0.2, 'G', fontsize=15)
        ax.scatter(0, self.p_, s=50, marker='o', color='black')
        ax.text(0.2, self.p_ + 0.2, 'F', fontsize=15)
        ax.scatter(self.intersection_x, 0, s=60, marker='o', color='black')
        ax.text(self.intersection_x+0.2, 0.2, 'H', fontsize=15)
        ax.fill_between([0, self.intersection_x, 0], [self.c_val+self.k, self.intersection_y, self.p_], [0, 0, 0], where=[True, True, True], interpolate=True, color='blue', alpha=0.2)
        xticks = np.arange(1, 15, 2)
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticks)
        yticks = np.arange(1, 15, 2)
        ax.set_yticks(yticks)
        ax.set_yticklabels(yticks)
        ax.set_xlim([0, 14])
        ax.set_ylim([0, 14])
        plt.gca().set_aspect('equal', adjustable='box')
        ax.set_title('Cournot competition - consumer profits and social profits')
        ax.set_xlabel('$x$')
        ax.set_ylabel('$p$')
        ax.legend(loc='upper right');



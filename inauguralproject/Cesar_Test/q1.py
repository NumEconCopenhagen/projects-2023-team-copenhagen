
import numpy as np
from scipy import optimize
from types import SimpleNamespace

class Rate_Work_at_Home:
   
    def __init__(self):
        par = self.par = SimpleNamespace()
        sol = self.sol = SimpleNamespace()
        
        #in this part we create the fixed parameters
        par.sigma = np.array([0.5,1.0,1.5])  #the example only included the case where sigma = 1, but here we put all the options
        par.alpha = np.array([0.25,0.50,0.75])

        par.epsilon = 1.0
        par.rho = 2.0
        par.nu = 0.001
        par.omega = 0.5

        #the wages
        par.wfemale = 1
        par.wmale = 1

        #solutions
        #market labour
        #we create vectors of zeros because we want to store the value for each iteration
        sol.LM_vec = np.zeros(5)
        sol.LF_vec = np.zeros(5)
        #home labour
        sol.HM_vec = np.zeros(5)
        sol.HF_vec = np.zeros(5)

    def utility(self,LM,HM,LF,HF):
        par = self.par 
        sol = self.sol
        
        #total market goods
        C = par.wfemale*LF + par.wmale*LM
        #output house
        #we need to create a condition so the prod. function changes depending on the value of epsilon
        for sigma in par.sigma:
                if sigma == 1.0:
                    for alpha in par.alpha:
                        H = HM**(1-alpha) * HF**alpha   
                        return H    
                else:
                    for alpha in par.alpha:
                        H = ((1-alpha)*HM**((sigma-1)/sigma) + alpha*HF**((sigma-1)/sigma))**(sigma/(sigma-1))
                        return H
        
        #total output
        Q = C**par.omega * H**(1-par.omega)
    
    #create a function for the discrete problem
    #so in order to have the values of L,H we need to apply the formula given inthe PDF and then put that numbers in the zero vectors
    def solve_discrete(self,do_print=False):
        """ solve model discretely """
        
        par = self.par
        sol = self.sol
        opt = SimpleNamespace()
        
        # a. all possible choices
        x = np.linspace(0,24,49)
        LM,HM,LF,HF = np.meshgrid(x,x,x,x) # all combinations
    
        LM = LM.ravel() # vector
        HM = HM.ravel()
        LF = LF.ravel()
        HF = HF.ravel()

        # b. calculate utility
        u = self.calc_utility(LM,HM,LF,HF)
    
        # c. set to minus infinity if constraint is broken
        I = (LM+HM > 24) | (LF+HF > 24) # | is "or"
        u[I] = -np.inf
    
        # d. find maximizing argument
        j = np.argmax(u)
        
        opt.LM = LM[j]
        opt.HM = HM[j]
        opt.LF = LF[j]
        opt.HF = HF[j]

        # e. print
        if do_print:
            for k,v in opt.__dict__.items():
                print(f'{k} = {v:6.4f}')

        return opt
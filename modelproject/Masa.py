import numpy as np
import matplotlib.pyplot as plt

class CournotCompetition:
    
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

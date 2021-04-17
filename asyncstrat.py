from threading import Thread
from localsearch import *
import numpy as np


if __name__ == '__main__':
    best_sol = np.full((n_bound,m_bound), False)
    best_value = 0


    Thread(target = main).start()
    Thread(target = main).start()

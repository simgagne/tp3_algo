
import colorama
import numpy as np
import copy
import random
import time
# import math
def color_sign(x):
    c = colorama.Fore.GREEN if x > 0 else colorama.Fore.RED
    return f'{c}{x}'

def dig(n, m, sol):
    start = m
    end = m + 1
    for i in reversed(range(n +1)):
        # if np.all(sol[i] == 1):
        #     print('dig shortcutt')
        #     break
        # for j in range(start,end):
        sol[i][start:end] = True
        start = (start -1) if (start -1) >=0  else start
        end = (end +1) if (end +1) <= len(sol[0]) else end
def fill(n, m, sol):
    start = m
    end = m+1
    for i in range(n, len(sol)):
        if not np.any(sol[i]):
            break
        # for j in range(start, end):
        sol[i][start:end] = False
        start = (start -1) if (start -1) >=0  else start
        end = (end +1) if (end +1) <= len(sol[0]) else end
def print_sol(sol):
    for i in range(len(sol)):
        for j in range(len(sol[0])):
            if sol[i][j]:
                print(i, j, flush=True)
def evaluate(sol, blocks_ratio):
    cost = 0

    cost = np.sum(blocks_ratio[sol])
    return cost
def evaluate_old(sol, blocks_ratio):
    cost = 0
    for i in range(len(blocks_ratio)):
        for j in range(len(blocks_ratio[0])):
            if sol[i][j]:
                cost += blocks_ratio[i][j]
    return cost

def parce_ground(filename):
    with open(filename, "r") as l:
        lines = l.readlines()
    blocks_value = []
    blocks_cost = []
    # for line in lines:
    #     print(line)
    depth = (int(lines.pop(0).split()[0]))
    for i in range(depth):
        as_list = lines[i].split()
        as_list = [int(j) for j in as_list]
   
        blocks_value.append(as_list)
    for i in range(depth, 2*depth):
        as_list = lines[i].split()
        as_list = [int(j) for j in as_list]
        blocks_cost.append(as_list)
    # print(blocks_value)
    # print(blocks_cost)
    blocks_ratio = np.subtract(np.array(blocks_value),  np.array(blocks_cost))
    return blocks_ratio
    # print(blocks_ratio)
def move( next,sol):
    n,m = next
    if sol[n][m]:
        fill(n,m, sol)
    else:
        dig(n,m, sol)
# def next_move(n,m,n_bound,m_bound, sol, current_value, blocks_ratio):
  

#     return options

# def select_neighboor(options):
#     return options.pop(random.randrange(len(options)))
def explore(n, m, n_bound, m_bound, mask):

    mask = copy.deepcopy(mask)
    min_n = n-1
    max_n = n+1
    min_m = m-1
    max_m = m+1

    explore = np.array([[(n-1,m-1),(n-1,m),(n-1,m+1)],
                        [(n,m-1),(n,m),(n,m+1)],
                        [(n+1,m-1),(n+1,m),(n+1,m+1)]], dtype = tuple)


    # print(explore)
    if max_m >= m_bound:
        mask[:,2] = False
    
    if min_m < 0:
        mask[:,0] = False


    if max_n >= n_bound:
        mask[2] = False

    if min_n < 0:
        mask[0] = False

    return explore[mask]

if __name__ == "__main__":
    # np.set_printoptions(formatter={'int': color_sign})
    start = time.time()
    blocks_ratio = parce_ground('./N900_M1200') 
    
    n_bound, m_bound = blocks_ratio.shape
    comp = np.full((n_bound, m_bound),True)
    comp_cost = evaluate(comp, blocks_ratio)
    best_solution = np.full((n_bound,m_bound), False)
    best_value = evaluate(best_solution, blocks_ratio) 
    next_mask = None
    nb_restart = 1000
    to_visit = []
    full = np.array([[True,True,True],
                     [True,True,True],
                     [True,True,True]], dtype= bool) 
    no = np.array([[True,True,True],
                 [False, False,False],
                 [False, False,False]], dtype= bool)
    s = np.array([[False, False,False],
                  [False, False,False],
                  [True,True,True]], dtype= bool)
    e = np.array([[False,False,True],
                  [False, False,True],
                  [False, False,True]], dtype= bool)
    w = np.array([[True,False,False],
                 [True, False,False],
                 [True, False,False]], dtype= bool)
    se = np.array([[False, False,False],
                   [False, False,True],
                   [False,True,True]], dtype= bool)
    sw = np.array([[False,False,False],
                   [True, False,False],
                   [True, True,False]], dtype= bool)
    ne = np.array([[False,True,True],
                   [False, False,True],
                   [False, False,False]], dtype= bool)
    nw = np.array([[True,True,False],
                   [True, False,False],
                   [False, False,False]], dtype= bool)


    for i in range(n_bound):
        for j in range(m_bound):
            to_visit.append((i,j))
   

    for i in range(nb_restart):

        print(nb_restart - i)
        if not len(to_visit):
            break
        n,m = to_visit.pop(random.randrange(len(to_visit)))

        next_explore = explore(n,m,n_bound, m_bound,full)
        better = True
        while better:
            # failed = 0
            
            better = False
           
            best_neighboor_value = None

            # for i in range(min_n, max_n):
            #     for j in range(min_m, max_m):
            if len(next_explore):
                
                for i in next_explore:
                    temp_sol = copy.deepcopy(best_solution)
                    move(i,temp_sol)
                        # print(temp_sol)

                    temp_value = evaluate(temp_sol, blocks_ratio)
                    if not best_neighboor_value or temp_value > best_neighboor_value:
                        best_neighboor_value = temp_value
                        best_neighboor_sol = temp_sol
                        best_n, best_m = i
                        
                        
                
                if best_neighboor_value > best_value:
                    best_value = best_neighboor_value
                    best_solution = best_neighboor_sol

                    if best_n > n:
                        if best_m > m:
                            next_mask = se
                        elif best_m < m:
                            next_mask = sw
                        else:
                            next_mask = s
                    elif best_n < n:
                        if best_m > m:
                            next_mask = ne
                        elif best_m < m:
                            next_mask = nw
                        else:
                            next_mask = no
                    else:
                        if best_m > m:
                            next_mask = e
                        elif best_m < m:
                            next_mask = w
                    next_explore = explore(best_n, best_m, n_bound, m_bound,next_mask)

                    if not(best_n == n and best_m == m):
                        better = True
                        n = best_n
                        m = best_m

                

       

    print(best_value)
    end =time.time()
    # print(best_solution)
    
    #print_sol(best_solution)
    print(comp_cost)
    print(end-start)
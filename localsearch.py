
import numpy as np
import copy
import random
import time
import sys


def dig(n, m, sol):
    start = m
    end = m + 1
    for i in reversed(range(n +1)):
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


def parce_ground(filename):
    with open(filename, "r") as l:
        lines = l.readlines()
    blocks_value = []
    blocks_cost = []
    
    depth = (int(lines.pop(0).split()[0]))
    for i in range(depth):
        as_list = lines[i].split()
        as_list = [int(j) for j in as_list]
   
        blocks_value.append(as_list)
    for i in range(depth, 2*depth):
        as_list = lines[i].split()
        as_list = [int(j) for j in as_list]
        blocks_cost.append(as_list)
    blocks_ratio = np.subtract(np.array(blocks_value),  np.array(blocks_cost))
    return blocks_ratio
def move(n,m,sol):
    if sol[n][m]:
        fill(n,m, sol)
    else:
        dig(n,m, sol)


if __name__ == "__main__":
    path = sys.argv[1]
    start = time.time()
    blocks_ratio = parce_ground(path) 
    
    n_bound, m_bound = blocks_ratio.shape
    comp = np.full((n_bound, m_bound),True)
    comp_cost = evaluate(comp, blocks_ratio)
    best_solution = np.full((n_bound,m_bound), False)
    best_value = evaluate(best_solution, blocks_ratio) 
    nb_restart = 1000
    to_visit = []
    for i in range(n_bound):
        for j in range(m_bound):
            to_visit.append((i,j))
   

    while(time.time() - start < 170):

        if not len(to_visit):
            break
        n,m = to_visit.pop(random.randrange(len(to_visit)))
       
        better = True
        while better:
            
            better = False
            min_n = n-1
            max_n = n+2
            min_m = m-1
            max_m = m+2

            max_m = m_bound  if max_m >= m_bound else max_m
            min_m = 0 if min_m < 0 else min_m

            max_n = n_bound  if max_n >= n_bound else max_n
            min_n = 0 if min_n < 0 else min_n
            best_neighboor_value = None

            for i in range(min_n, max_n):
                for j in range(min_m, max_m):
                    temp_sol = copy.deepcopy(best_solution)
                    move(i,j,temp_sol)

                    temp_value = evaluate(temp_sol, blocks_ratio)
                    if not best_neighboor_value or temp_value > best_neighboor_value:
                        best_neighboor_value = temp_value
                        best_neighboor_sol = temp_sol
                        n = i
                        m = j
                    
            
            if best_neighboor_value > best_value:
                best_value = best_neighboor_value
                best_solution = best_neighboor_sol
                better = True

    print_sol(best_solution)
    
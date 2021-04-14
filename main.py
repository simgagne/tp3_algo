
import colorama
import numpy as np
import copy
import random
import time
import math
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
        for j in range(start,end):
            sol[i][j] = 1
        start = (start -1) if (start -1) >=0  else start
        end = (end +1) if (end +1) <= len(sol[0]) else end
def fill(n, m, sol):
    start = m
    end = m+1
    for i in range(n, len(sol)):
        if not np.any(sol[i]):
            break
        for j in range(start, end):
            sol[i][j] = 0
        start = (start -1) if (start -1) >=0  else start
        end = (end +1) if (end +1) <= len(sol[0]) else end
def print_sol(sol):
    for i in range(len(sol)):
        for j in range(len(sol[0])):
            if sol[i][j]:
                print(i, j, flush=True)
def evaluate(sol, blocks_ratio):
    cost = 0
    for i in range(len(blocks_ratio)):
        if not np.any(sol[i]):
            break
        for j in range(len(blocks_ratio[0])):
            if sol[i][j]:
                cost += blocks_ratio[i][j]
    return cost
def evaluate_old(sol, blocks_ratio):
    cost = 0
    for i in range(len(blocks_ratio)):
        for j in range(len(blocks_ratio[0])):
            if sol[i][j]:
                cost += blocks_ratio[i][j]
    return cost

def parce_building(filename):
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
        #as_list = as_list.replace("\n", "")
    #     as_list = [int(j) for j in as_list]
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
def move(n,m,sol):
    if sol[n][m]:
        fill(n,m, sol)
    else:
        dig(n,m, sol)



if __name__ == "__main__":
    # np.set_printoptions(formatter={'int': color_sign})
    start = time.time()
    blocks_ratio = parce_building('./N200_M100') 
    
    n_bound, m_bound = blocks_ratio.shape
    comp = np.ones((len(blocks_ratio), len(blocks_ratio[0])),dtype=int)
    comp_cost = evaluate(comp, blocks_ratio)
    best_solution = np.zeros((len(blocks_ratio), len(blocks_ratio[0])),dtype=int)
    best_value = evaluate(best_solution, blocks_ratio) 
    nb_restart = 50
    limit = 5
    itterations = 1000
    init_temp = 10
    

    for i in range(nb_restart):
        sol = copy.deepcopy(best_solution)
        value = copy.deepcopy(best_value)

        t = init_temp
        n = random.randrange(0,len(blocks_ratio))
        m = random.randrange(0,len(blocks_ratio[0]))
        # sol_cost = evaluate(sol, blocks_ratio)
        for j in range(itterations):
            failed = 0
            

            # m = j % len(blocks_ratio[0])
            temp_sol = copy.deepcopy(sol)
            temp_value = copy.deepcopy(value)


            # temp_n = random.randrange(n-2, n+3)
            # temp_n = n_bound -1 if temp_n >= n_bound else temp_n
            # temp_n = 0 if temp_n < 0 else temp_n
            
            # temp_m = random.randrange(m-2, m+3)
            # temp_m = m_bound -1 if temp_m >= m_bound else temp_m
            # temp_m = 0 if temp_m < 0 else temp_m



            #move(temp_n,temp_m,temp_sol)
            move(n,m,temp_sol)
            
            temp_value = evaluate(temp_sol,blocks_ratio)
            delta = value - temp_value  

            if delta < 0 or random.random() < math.exp(-delta/t):
                sol = temp_sol
                value = temp_value
                failed = 0
                # m = temp_m
                # n = temp_n
                print(sol)

                if value > best_value:
                    best_value = value
                    best_solution = sol
            else:
                failed+=1
                if failed > limit:
                    break
            
            t = 0.999*t


            n = random.randrange(n-2, n+3)
            n = n_bound -1 if n >= n_bound else n
            n = 0 if n < 0 else n
            
            m = random.randrange(m-2, m+3)
            m = m_bound -1 if m >= m_bound else m
            m = 0 if m < 0 else m

    print(best_value)
    end =time.time()
    print(best_solution)
    
    #print_sol(best_solution)
    print(comp_cost)
    # print(end-start)
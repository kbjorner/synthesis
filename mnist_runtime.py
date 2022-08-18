import time, os
import pandas as pd
import random
from tqdm import tqdm
import matplotlib.pyplot as plt
from generate_graphs import mnist_runtime_graph

def createFile(constraints_ind):
    # g = open("smtfiles/mnist_myconstrs.txt", "rt")
    g = open("smtfiles/mnist_constraints.smt2", "rt")
    all_constraints = g.readlines()
    g.close()
    auxfile1 = 'mnist_aux_input.smt2'
    auxfile2 = 'mnist_aux_output.smt2'
    f = open(auxfile1, 'w')
    # have this in a file to read from
    h = open("smtfiles/mnist_grammar.smt2", "r")
    for line in h:
        f.write(line)
    # print('done with the grammar')
    for j in constraints_ind:
        f.write(all_constraints[j])

    f.write("(check-synth)")
    f.close()

    start_time = time.time()
    os.system(f'../cvc5-Linux --lang=sygus2 {auxfile1} >{auxfile2}')
    os.remove(auxfile1)
    os.remove(auxfile2)

    runTime = time.time() - start_time
    
    # runs through getStates function to use for mean calculation
    return runTime  


def run_benchmark(n, iterate, runtime_data):
    for i in tqdm(range(len(iterate))):
        num_constraints = iterate[i]
        arr_constraints = [] # size i in iterate
        
        for i in tqdm(range(1,11), leave=False):
            arr_constraints = random.sample(range(0,153), num_constraints)
            timeRun = createFile(arr_constraints)
            runtime_data.loc[i,num_constraints] = timeRun
    
    runtime_data.to_csv('data/mnist_runtime.csv')


def main():
    n = 10
    iterate = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    runtime_data = pd.DataFrame(columns=iterate, index=range(1,n+1))
    run_benchmark(n, iterate, runtime_data)
    mnist_runtime_graph( )
    plt.show()
if __name__ == "__main__":
    main()
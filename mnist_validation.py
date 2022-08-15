import time, os
import numpy as np, pandas as pd
import random
from tqdm import tqdm

def createFile(constraints_ind):
    # g = open("smtfiles/mnist_myconstrs.txt", "rt")
    g = open("smtfiles/mnist_constraints.txt", "rt")
    all_constraints = g.readlines()
    g.close()
    # print(constraints)
    f = open('mnist.smt2', 'w')
    # have this in a file to read from
    h = open("smtfiles/mnist_grammar.txt", "r")
    for line in h:
        f.write(line)
    # print('done with the grammar')
    for j in constraints_ind:
        f.write(all_constraints[j])

    f.write("(check-synth)")
    f.close()

    start_time = time.time()
    os.system('../cvc5-Linux --lang=sygus2 mnist.smt2 >mimic.smt2')

    runTime = time.time() - start_time
    
    # runs through getStates function to use for mean calculation
    return runTime  


def run_benchmark(n, iterate, runtime_data):
    for i in tqdm(range(len(iterate))):
        num_constraints = iterate[i]
        arr_constraints = [] # size i in iterate
        
        for i in range(1,11):
            arr_constraints = random.sample(range(0,153), num_constraints)
            timeRun = createFile(arr_constraints)
            runtime_data.loc[i,num_constraints] = timeRun
    
    runtime_data.to_csv('mnist_runtime.csv')




def main():
    num_constraints = 10
    with open("smtfiles/mnist_constraints.txt", "rt") as g:
        all_constraints = g.readlines()
    arr_constraints = random.sample(range(0,len(all_constraints)), num_constraints)
    createFile(arr_constraints)
    


if __name__ == "__main__":
    main()
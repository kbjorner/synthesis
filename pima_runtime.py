import time, os, random
from tqdm import tqdm
import pandas as pd
from generate_runtime_graphs import pima_runtime_graph
import matplotlib.pyplot as plt


def createFile(constraints_ind, grammar_type):
    g = open("smtfiles/pima_constraints.txt", "rt")
    all_constraints = g.readlines()
    g.close()
    # print(constraints)
    auxfile1 = 'pima_aux_input.smt2'
    auxfile2 = 'pima_aux_output.smt2'
    f = open(auxfile1, 'w')
    # have this in a file to read from
    h = open(f"smtfiles/pima_grammar_{grammar_type}.smt2", "r")
    for line in h:
        f.write(line)
    for j in constraints_ind:
        f.write(all_constraints[j])

    f.write("(check-synth)")
    f.close()

    start_time = time.time()
    os.system(f'../cvc5-Linux --lang=sygus2 {auxfile1} >{auxfile2}')
    os.remove(auxfile1)
    os.remove(auxfile2)

    runTime = time.time() - start_time    
    return runTime  


def run_benchmark(n, iterate, runtime_data):
    for grammar_type in {"simple", "bootstrap"}:
        for num_constraints in tqdm(iterate):
            arr_constraints = [] # size i in iterate
            
            for i in tqdm(range(1,11),leave=False):
                arr_constraints = random.sample(range(0,153), num_constraints)
    #             print(arr_constraints)
                timeRun = createFile(arr_constraints, grammar_type=grammar_type)
                runtime_data.loc[i,num_constraints] = timeRun
        
        runtime_data.to_csv(f'data/pima_runtime_{grammar_type}.csv')


def main():
    n = 10
    iterate = [20, 40, 60, 80, 100, 120, 140]
    runtime_data = pd.DataFrame(columns=iterate, index=range(1,n+1))
    run_benchmark(n, iterate, runtime_data)
    pima_runtime_graph()
    plt.show()

if __name__ == "__main__":
    main()
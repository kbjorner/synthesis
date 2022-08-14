import time, os
import numpy as np, pandas as pd
import random

def createFile(constraints_ind):
    # g = open("smtfiles/mnist_myconstrs.txt", "rt")
    g = open("smtfiles/pima_constraints.txt", "rt")
    all_constraints = g.readlines()
    g.close()
    # print(constraints)
    f = open('pima.smt2', 'w')
    # have this in a file to read from
    h = open("smtfiles/pima_grammar.txt", "r")
    for line in h:
        f.write(line)
    print('done with the grammar')
    for j in constraints_ind:
        f.write(all_constraints[j])

    f.write("(check-synth)")
    f.close()

    start_time = time.time()
    os.system('../cvc5-Linux --lang=sygus2 pima.smt2 >mimic.smt2')

    runTime = time.time() - start_time
    
    # runs through getStates function to use for mean calculation
    return runTime  

# def getStates():
#     # run 10 times each iterate number to get 5 num summary and plot mean with variance
#     for num_constraints in iterate:
#         arr_constraints = [] # size i in iterate
#         arr_runtimes = [] # size n
#         print("new constraints used")
        
#         for i in range(1,11):
#             arr_constraints = random.sample(range(0,2163), num_constraints)
# #             print(arr_constraints)
#             timeRun = createFile(arr_constraints)
#             mnist_runtime.loc[i,num_constraints] = timeRun
#             arr_runtimes.append(timeRun)
#             arr_constraints = []
    
#     mnist_runtime.to_csv('synth_runtime_anal.csv')


def run_benchmark(n, iterate, runtime_data):
    for num_constraints in iterate:
        arr_constraints = [] # size i in iterate
        print("new constraints used")
        
        for i in range(1,11):
            arr_constraints = random.sample(range(0,153), num_constraints)
#             print(arr_constraints)
            timeRun = createFile(arr_constraints)
            runtime_data.loc[i,num_constraints] = timeRun
    
    runtime_data.to_csv('synth_runtime_anal.csv')




def main():
    n = 10
    iterate = [20, 40, 60, 80, 100, 120, 140]
    runtime_data = pd.DataFrame(columns=iterate, index=range(1,n+1))
    run_benchmark(n, iterate, runtime_data)
    # arr_constraints = [] # size i in iterate
    # print("new constraints used")
    # arr_constraints = random.sample(range(0,153), num_constraints)
    # timeRun = createFile(arr_constraints)
    # print(timeRun)

if __name__ == "__main__":
    main()
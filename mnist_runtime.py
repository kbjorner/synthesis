import time, os, yaml, subprocess
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

    with open('config.yml', 'r') as cf:
        cvc5path = yaml.load(cf, Loader=yaml.FullLoader)['cvc5']

    start_time = time.time()

    with open(auxfile2, 'w') as f_out:
        subprocess.run([cvc5path, '--lang=sygus2', auxfile1], stdout=f_out)
    
    # Read the contents of auxfile2
    with open(auxfile2, 'r') as f:
        auxfile2_contents = f.read()

    print(auxfile2_contents)

    num_nodes = 0
    target_word = "ite"
    index = auxfile2_contents.find(target_word)
    decision_tree1 = auxfile2_contents[index + len(target_word):]
    decision_tree2 = auxfile2_contents[index + len(target_word):]

    g_e = "<="
    ge_index = decision_tree1.find(g_e)
    while ge_index != -1:
        num_nodes += 1
        decision_tree1 = decision_tree1[ge_index + len(g_e):]
        ge_index = decision_tree1.find(g_e)

    let = "_let"
    let_index = decision_tree2.find(let)
    while let_index != -1:
        num_nodes += 1
        decision_tree2 = decision_tree2[let_index + len(let):]
        let_index = decision_tree2.find(let)

    print(num_nodes)

    decision_tree = auxfile2_contents[index - 1:]
    print(decision_tree)

    tree_depth = count_tree_depth(decision_tree)
    print(tree_depth)

    os.remove(auxfile1)
    os.remove(auxfile2)

    runTime = time.time() - start_time
    
    # runs through getStates function to use for mean calculation
    return runTime, num_nodes, tree_depth

def count_tree_depth(tree_str):
    max_depth = 0
    current_depth = 0

    for char in tree_str:
        if char == "(":
            current_depth += 1
            max_depth = max(max_depth, current_depth)
        elif char == ")":
            current_depth -= 1

    return max_depth


def run_benchmark(n, iterate, runtime_data, treedepth_data, numnodes_data):
    for i in tqdm(range(len(iterate))):
        num_constraints = iterate[i]
        arr_constraints = [] # size i in iterate
        
        for i in tqdm(range(1,11), leave=False):
            arr_constraints = random.sample(range(0,153), num_constraints)
            timeRun, numNodes, treeDepth = createFile(arr_constraints)
            runtime_data.loc[i,num_constraints] = timeRun
            numnodes_data.loc[i,num_constraints] = numNodes
            treedepth_data.loc[i,num_constraints] = treeDepth
    
    runtime_data.to_csv('data/mnist_runtime.csv')
    numnodes_data.to_csv('data/mnist_numnodes.csv')
    treedepth_data.to_csv('data/mnist_treedepth.csv')


def main():
    # n = 10
    n = 1
    # iterate = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    iterate = [10]
    runtime_data = pd.DataFrame(columns=iterate, index=range(1,n+1))
    treedepth_data = pd.DataFrame(columns=iterate, index=range(1,n+1))
    numnodes_data = pd.DataFrame(columns=iterate, index=range(1,n+1))
    run_benchmark(n, iterate, runtime_data, treedepth_data, numnodes_data)
    # mnist_runtime_graph()
    # plt.show()
if __name__ == "__main__":
    main()
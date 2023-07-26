import time, os, random, yaml, subprocess, datetime
from tqdm import tqdm
import pandas as pd
from generate_graphs import pima_runtime_graph
import matplotlib.pyplot as plt


def createFile(constraints_ind, grammar_type):
    g = open("smtfiles/pima_constraints.smt2", "rt")
    all_constraints = g.readlines()
    g.close()
    # print(constraints)
    inputfile = 'pima_aux_input.smt2'
    outputfile = 'pima_aux_output.smt2'
    f = open(inputfile, 'w')
    # have this in a file to read from
    h = open(f"smtfiles/pima_grammar_{grammar_type}.smt2", "r")
    for line in h:
        f.write(line)
    for j in constraints_ind:
        f.write(all_constraints[j])

    f.write("(check-synth)")
    f.close()

    with open('config.yml', 'r') as cf:
        cvc5path = yaml.load(cf, Loader=yaml.FullLoader)['cvc5']

    start_time = time.time()
    with open(outputfile, 'w') as foo:
        # p = subprocess.Popen(f'{cvc5path} --lang=sygus2 {inputfile} >{outputfile}', shell=True)
        p = subprocess.Popen([f'{cvc5path}', '--lang=sygus2', inputfile], stdout=foo, shell=False)
        try:
            p.wait(3)
        except:
            p.kill()
            bugreport = f"Bugreport:\n\tgrammar_type: {grammar_type},\n\tnumber_of_constraints: {len(constraints_ind)},\n\tconstraints_ind: {constraints_ind}\n"
            with open(inputfile, 'r') as fp:
                bugreport += f"\tinputfile: \n {fp.read()}"
            timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            with open(f'bugreport_{timestamp}.txt', 'w') as out:
                print(bugreport, file=out)
            # print("Had to kill one\n")

        # os.system(f'{cvc5path} --lang=sygus2 {inputfile} >{outputfile}')

        # Read the contents of auxfile2
    with open(outputfile, 'r') as f:
        auxfile2_contents = f.read()


    num_nodes = 0
    target_word = "ite"
    index = auxfile2_contents.find(target_word)
    decision_tree1 = auxfile2_contents[index + len(target_word):]
    decision_tree2 = auxfile2_contents[index + len(target_word):]
    decision_tree3 = auxfile2_contents[index + len(target_word):]
    decision_tree4 = auxfile2_contents[index + len(target_word):]
    decision_tree5 = auxfile2_contents[index + len(target_word):]

    g_e = ">="
    ge_index = decision_tree1.find(g_e)
    while ge_index != -1:
        num_nodes += 1
        decision_tree1 = decision_tree1[ge_index + len(g_e):]
        ge_index = decision_tree1.find(g_e)

    l_e = "<="
    le_index = decision_tree2.find(l_e)
    while le_index != -1:
        num_nodes += 1
        decision_tree2 = decision_tree2[le_index + len(l_e):]
        le_index = decision_tree2.find(l_e)

    node_true = "true"
    true_index = decision_tree3.find(node_true)
    while true_index != -1:
        num_nodes += 1
        decision_tree3 = decision_tree3[true_index + len(node_true):]
        true_index = decision_tree3.find(node_true)

    node_false = "false"
    false_index = decision_tree4.find(node_false)
    while false_index != -1:
        num_nodes += 1
        decision_tree4 = decision_tree4[false_index + len(node_false):]
        false_index = decision_tree4.find(node_false)

    let = "_let"
    let_index = decision_tree5.find(let)
    while let_index != -1:
        num_nodes += 1
        decision_tree5 = decision_tree5[let_index + len(let):]
        let_index = decision_tree5.find(let)

    print(f"nodes: {num_nodes}")

    decision_tree = auxfile2_contents[index - 1:]
    print(decision_tree)

    tree_depth = count_tree_depth(decision_tree)
    print(f"depth: {tree_depth}")



    # os.system(f'{cvc5path} --lang=sygus2 {inputfile} >{outputfile}')
    # os.remove(inputfile)
    # os.remove(outputfile)

    runTime = time.time() - start_time    
    return runTime, num_nodes, tree_depth

def count_tree_depth(tree_str):
    max_depth = 0
    current_depth = 0
    in_division = False
    stack = []

    for char in tree_str:
        if char == "(":
            stack.append(char)
            current_depth += 1
            max_depth = max(max_depth, current_depth)
        elif char == ")":
            if stack:
                stack.pop()
            current_depth -= 1
        elif char == "/":
            in_division = True
        elif char == " " and in_division:
            in_division = False

    return max_depth

def run_benchmark(n, iterate, runtime_data, numnodes_data, treedepth_data):
    for grammar_type in {"simple", "bootstrap"}:
        for num_constraints in tqdm(iterate):
            arr_constraints = [] # size i in iterate
            
            for i in tqdm(range(1,n+1),leave=False):
                arr_constraints = random.sample(range(0,153), num_constraints)
    #             print(arr_constraints)
                timeRun, numNodes, treeDepth = createFile(arr_constraints, grammar_type=grammar_type)
                runtime_data.loc[i,num_constraints] = timeRun
                numnodes_data.loc[i,num_constraints] = numNodes
                treedepth_data.loc[i,num_constraints] = treeDepth

        
        runtime_data.to_csv(f'data/pima_runtime_{grammar_type}.csv')
        numnodes_data.to_csv(f'data/pima_numnodes_{grammar_type}.csv')
        treedepth_data.to_csv(f'data/pima_treedepth_{grammar_type}.csv')


def main():
    # n = 10
    n = 1
    # iterate = [20, 40, 60, 80, 100, 120, 140]
    iterate = [10]
    runtime_data = pd.DataFrame(columns=iterate, index=range(1,n+1))
    numnodes_data = pd.DataFrame(columns=iterate, index=range(1,n+1))
    treedepth_data = pd.DataFrame(columns=iterate, index=range(1,n+1))
    run_benchmark(n, iterate, runtime_data, numnodes_data, treedepth_data)
    # pima_runtime_graph()
    # plt.show()

if __name__ == "__main__":
    main()
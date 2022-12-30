import os, random, statistics, subprocess, datetime
import yaml
import pandas as pd
from tqdm import tqdm
from generate_graphs import pima_treestats_graph



def ites(data):
    counter = 0
    for i in range(3, len(data)):
        if data[i-3:i] == "ite":
            counter += 1
    return counter

# def leaves(data):


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

    with open(outputfile, 'w') as foo:
        # p = subprocess.Popen(f'{cvc5path} --lang=sygus2 {inputfile} >{outputfile}', shell=True)
        p = subprocess.Popen([f'{cvc5path}', '--lang=sygus2', inputfile], stdout=foo, shell=False)
        hadtokill = False
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
            hadtokill = True
            # print("Had to kill one\n")

    if not hadtokill:
        os.system(f'cp {outputfile} something.txt')
    # os.system(f'{cvc5path} --lang=sygus2 {inputfile} > {outputfile}') # >{outputfile}
    # os.remove(inputfile)
    # os.remove(outputfile)

def run_treestats_benchmark(n, iterate, treestats_data):
    for grammar_type in {"simple", "bootstrap"}:
        for num_constraints in tqdm(iterate):
            arr_constraints = [] # size i in iterate
            
            for i in tqdm(range(1,n+1),leave=False):
                arr_constraints = random.sample(range(0,153), num_constraints)
    #             print(arr_constraints)
                createFile(arr_constraints, grammar_type=grammar_type)
                with open('pima_aux_output.smt2', 'r') as file:
                    data = file.read().replace('\n', '')
                    treestats_data.loc[i,num_constraints] = ites(data)
        
        treestats_data.to_csv(f'data/pima_treestats_{grammar_type}.csv')


def count_grammar_nodes():
    with open('smtfiles/pima_grammar_bootstrap.smt2', 'r') as fp:
        data = fp.readlines()
        number_of_nodes = 0
        for line in data:
            if line.count('Real') == 1:
                line = line.replace('(', ' ')
                line = line.replace(')', ' ')
                for i in line.split(' '):
                    if i.replace('.','').isnumeric():
                        number_of_nodes += 1
    return number_of_nodes

def main():
    n = 10
    iterate = [20, 40, 60, 80, 100, 120, 140]
    results_bootstrap = []
    results_simple = []

    treestats_data = pd.DataFrame(columns=iterate, index=range(1,n+1))
    run_treestats_benchmark(n,iterate,treestats_data)
    pima_treestats_graph()
    print('done')
    # for i in range(n):
    #     for grammar_type in {"simple", "bootstrap"}:
    #         arr_constraints = random.sample(range(0,153), 140)
    #         createFile(arr_constraints, grammar_type=grammar_type)
    #         with open('pima_aux_output.smt2', 'r') as file:
    #             data = file.read().replace('\n', '')
    #             num_ites = ites(data)
    #         if grammar_type == "simple":
    #             results_simple.append(num_ites)
    #         else:
    #             results_bootstrap.append(num_ites)

    # bootstrap_mean = statistics.mean(results_bootstrap)
    # bootstrap_std = statistics.stdev(results_bootstrap)
    # simple_mean = statistics.mean(results_simple)
    # simple_std = statistics.stdev(results_simple)

    # print(f"BS mean: {bootstrap_mean}, std: {bootstrap_std}. S mean: {simple_mean}, std: {simple_std}")
    

if __name__ == "__main__":
    main()
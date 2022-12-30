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



    # os.system(f'{cvc5path} --lang=sygus2 {inputfile} >{outputfile}')
    # os.remove(inputfile)
    # os.remove(outputfile)

    runTime = time.time() - start_time    
    return runTime  


def run_benchmark(n, iterate, runtime_data):
    for grammar_type in {"simple", "bootstrap"}:
        for num_constraints in tqdm(iterate):
            arr_constraints = [] # size i in iterate
            
            for i in tqdm(range(1,n+1),leave=False):
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
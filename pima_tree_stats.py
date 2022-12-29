import os, random, statistics
import yaml


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

    with open('config.yml', 'r') as cf:
        cvc5path = yaml.load(cf, Loader=yaml.FullLoader)['cvc5']
    
    os.system(f'{cvc5path} --lang=sygus2 {auxfile1} > {auxfile2}') # >{auxfile2}
    # os.remove(auxfile1)
    # os.remove(auxfile2)

def main():
    n = 10
    # iterate = [20, 40, 60, 80, 100, 120, 140]
    results_bootstrap = []
    results_simple = []
    for i in range(n):
        for grammar_type in {"simple", "bootstrap"}:
            arr_constraints = random.sample(range(0,153), 140)
            createFile(arr_constraints, grammar_type=grammar_type)
            with open('pima_aux_output.smt2', 'r') as file:
                data = file.read().replace('\n', '')
                num_ites = ites(data)
            if grammar_type == "simple":
                results_simple.append(num_ites)
            else:
                results_bootstrap.append(num_ites)

    bootstrap_mean = statistics.mean(results_bootstrap)
    bootstrap_std = statistics.stdev(results_bootstrap)
    simple_mean = statistics.mean(results_simple)
    simple_std = statistics.stdev(results_simple)

    print(f"BS mean: {bootstrap_mean}, std: {bootstrap_std}. S mean: {simple_mean}, std: {simple_std}")
            

if __name__ == "__main__":
    main()
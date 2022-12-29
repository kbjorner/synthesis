from functools import total_ordering
import time, os, hy, yaml
import numpy as np, pandas as pd
import random, pickle
import subprocess, io
from tqdm import tqdm
from pima_NN import TrainingInstance
from matplotlib import pyplot as plt
from generate_graphs import make_pima_global_accuracy_graph

def remove_divisions(instring):
    resultstring = instring
    for i in range(len(instring)):
        if instring[i] == '/':
#             print(instring[])
            a = instring[i+2:].split(')')[0].split(' ')[0]
            b = instring[i+2:].split(')')[0].split(' ')[1]
            c = float(a)/float(b)
            resultstring = resultstring.replace(f'(/ {a} {b})', f'{c}', 1)
#             print(instring[i+2:].find(')'))
            
#             print(f"a is {a}, b is {b}, c is {c}")
    return resultstring

def nice_parenthesis(instring):
    result = ""
    currenttab = 0
    for i in instring:
        
        if i == '(':
            currenttab += 1
            result += "(\n"
            for j in range(currenttab):
                result += "\t"
        elif i == ')':
            currenttab -= 1
            result += "\n"
            for j in range(currenttab):
                result += "\t"
            result += ")"
        else:
            result +=i
    return result

def get_first_correct_parenthesis(instring):
    num_parenthesis = 1
    first_parenthesis = instring.find('(')
    if first_parenthesis == -1:
        last_parenthesis = instring.find(')')
        if last_parenthesis != 0:
            stripped_spaces = instring[0:last_parenthesis].split(' ')
            for i in range(len(stripped_spaces)):
                if len(stripped_spaces[i]) > 0:
                    return stripped_spaces[i]
        return instring
    last_parenthesis = first_parenthesis
    while num_parenthesis > 0:
        last_parenthesis += 1
        if instring[last_parenthesis] == '(':
            num_parenthesis += 1
        elif instring[last_parenthesis] == ')':
            num_parenthesis -= 1
    return instring[first_parenthesis:last_parenthesis+1]

def get_second_correct_parenthesis(instring):
    num_parenthesis = 1
    first_parenthesis = instring.find('(')
    if first_parenthesis == -1:
        last_parenthesis = instring.find(')')
        if last_parenthesis != 0:
            stripped_spaces = instring[0:last_parenthesis].split(' ')
            for i in range(len(stripped_spaces)):
                if len(stripped_spaces[i]) > 0:
                    return stripped_spaces[i]
        return instring
    last_parenthesis = first_parenthesis
    while num_parenthesis > 0:
        last_parenthesis += 1
        if instring[last_parenthesis] == '(':
            num_parenthesis += 1
        elif instring[last_parenthesis] == ')':
            num_parenthesis -= 1
    # print(f"Sent to find first parenthesis: {instring[last_parenthesis+1:].replace(' ','X')}")
    return get_first_correct_parenthesis(instring[last_parenthesis+1:])

def get_third_correct_parenthesis(instring):
    num_parenthesis = 1
    first_parenthesis = instring.find('(')
    if first_parenthesis == -1:
        last_parenthesis = instring.find(')')
        if last_parenthesis != 0:
            stripped_spaces = instring[0:last_parenthesis].split(' ')
            for i in range(len(stripped_spaces)):
                if len(stripped_spaces[i]) > 0:
                    return stripped_spaces[i]
        return instring
    last_parenthesis = first_parenthesis
    while num_parenthesis > 0:
        last_parenthesis += 1
        if instring[last_parenthesis] == '(':
            num_parenthesis += 1
        elif instring[last_parenthesis] == ')':
            num_parenthesis -= 1
    # print(f"Sent to find second parenthesis: {instring[last_parenthesis+1:].replace(' ','X')}")
    return get_second_correct_parenthesis(instring[last_parenthesis+1:])


def clean_mimic_program(mimic_smtfile):
    with open(mimic_smtfile, 'r') as g:
        raw = g.readlines()[1]
    raw = remove_divisions(raw)
    let_values = []
    variables = 1
    found = True
    while found:
        found = False
        startind = raw.find(f"_let_{variables}")
        
        if startind != -1:
            let_values.append(get_first_correct_parenthesis(raw[startind:]))
            variables += 1
            found =True
    if len(let_values) > 0:
        last_portion = raw[raw.find(let_values[-1])+len(let_values[-1]):]
    else:
        last_portion = raw
    for i in range(len(let_values)):
        for j in range(len(let_values)):
            let_values[j] = let_values[j].replace(f"_let_{i+1} ",f"{let_values[i]} ")
            let_values[j] = let_values[j].replace(f"_let_{i+1})",f"{let_values[i]})")

    
    for i in range(len(let_values)):
        last_portion = last_portion.replace(f"_let_{i+1} ",f"{let_values[i]} ")
        last_portion = last_portion.replace(f"_let_{i+1})",f"{let_values[i]})")
    ite = last_portion.find('ite')
    # print(f"Last portions: {last_portion[ite:]} \n")
    tree_first = get_first_correct_parenthesis(last_portion[ite:])
    tree_second = get_second_correct_parenthesis(last_portion[ite:])
    tree_third = get_third_correct_parenthesis(last_portion[ite:])
    # print(f"first: {tree_first}\n second: {tree_second}\n, third: {tree_third}\n")
    final = f"(ite {tree_first} {tree_second} {tree_third})"
    with open('diagnostic_mimic_program.txt', 'w') as fp:
        fp.write(final)

def classify_patient(values):
    file = open("diagnostic_mimic_program.txt", "r")
    data = file.read()
    file.close()
    data = data.replace('true', 'True')
    data = data.replace('false', 'False')

    data = data.replace("ite", "if")

    args = ""
    var_names = [ 
            'Pregnancies', 
            'Glucose', 
            'BloodPressure', 
            'SkinThickness', 
            'Insulin', 
            'BodyMassIndex', 
            'DiabetesPedigreeFunction', 
            'Age'
        ]
    for i, var in enumerate(var_names):
            args += "(setv {} {})".format(var, values[i])
            

    prog = args + data
    expr = hy.read(f"((fn [] {prog}))")
#     print(expr)
    return hy.eval(expr)


def createFile(constraints_ind, inputfile, outputfile, grammar_type):
    g = open("smtfiles/pima_constraints.smt2", "rt")
    all_constraints = g.readlines()
    g.close()
    # print(constraints)
    f = open(inputfile, 'w')
    h = open(f"smtfiles/pima_grammar_{grammar_type}.smt2", "r")
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
    with open(outputfile, 'w') as foo:
        # p = subprocess.Popen(f'{cvc5path} --lang=sygus2 {inputfile} >{outputfile}', shell=True)
        p = subprocess.Popen([f'{cvc5path}', '--lang=sygus2', inputfile], stdout=foo, shell=False)
        try:
            p.wait(10)
        except:
            p.kill()
            print("Had to kill one\n")

        # os.system(f'{cvc5path} --lang=sygus2 {inputfile} >{outputfile}')

    runTime = time.time() - start_time
    
    return runTime  


def mimic_program_global_accuracy(T):

    total_predictions = 0
    right_predictions_acc = 0
    right_predictions_rec = 0
    buffer = min(T.test_xs.index)
    for i in T.outcomes_df.index:
        values = list(T.test_xs.loc[i+buffer,:])
        program_outcome = classify_patient(values)
        ground_truth = T.test_ys.loc[i+buffer, 'Outcome'] > 0.5
        model_outcome = T.outcomes_df.loc[i,'prediction']
        if program_outcome == ground_truth:
            right_predictions_acc += 1
        if program_outcome == model_outcome:
            right_predictions_rec += 1
        total_predictions += 1

    return right_predictions_acc/total_predictions, right_predictions_rec/total_predictions 

    


# def get_accuracy(num_constraints, T):
#     index_array = list(range(num_constraints))
#     tempfile = 'smtfiles/temp_pima.smt2'
#     createFile(index_array, tempfile)
#     clean_mimic_program('pima_mimic.smt2')
#     model_accuracy = T.local_accuracy(index_array)
#     print(model_accuracy)
#     mimic_accuracy = mimic_program_global_accuracy(T)
#     print(mimic_accuracy)


def main():

    ### UNDER CONSTRUCTION
    T = TrainingInstance()
    T.data_preparation()
    with open('models/pima_model2.pkl', 'br') as fp:
        T.model = pickle.load(fp)
    T.make_constraints()
    T.computeMagicNumbers()
    inputfile = 'pima_aux_input.smt2'
    outputfile = 'pima_aux_output.smt2'
    constraints = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140]
    
    ### ONE TIME FOR BOOTSTRAP MAGIC NUMBERS

    grammar_type = "bootstrap"

    for grammar_type in {"bootstrap", "simple"}:
        # grammar_type = "bootstrap"
        global_accuracy = pd.DataFrame(columns=constraints)
        global_recall = pd.DataFrame(columns=constraints)
        for num_constraints in tqdm(constraints):
            createFile(list(range(num_constraints)), inputfile, outputfile, grammar_type)
            clean_mimic_program(outputfile)
            acc, rec = mimic_program_global_accuracy(T)
            global_accuracy.loc[0,num_constraints] = acc
            global_recall.loc[0,num_constraints] = rec
            global_accuracy.to_csv(f'data/pima_global_accuracy_{grammar_type}.csv')
            global_recall.to_csv(f'data/pima_global_recall_{grammar_type}.csv')

        make_pima_global_accuracy_graph(grammar_type=grammar_type)
        plt.show()
    
    # for some reason, keras load model doenst' work
    
if __name__ == "__main__":
    main()
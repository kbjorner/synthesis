from functools import total_ordering
import time, os, hy
import numpy as np, pandas as pd
import random, pickle
from tqdm import tqdm
from mnist_NN import TrainingInstance
from tensorflow import keras

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
            return instring[0:last_parenthesis]
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
            return instring[0:last_parenthesis]
        return instring
    last_parenthesis = first_parenthesis
    while num_parenthesis > 0:
        last_parenthesis += 1
        if instring[last_parenthesis] == '(':
            num_parenthesis += 1
        elif instring[last_parenthesis] == ')':
            num_parenthesis -= 1
    return get_first_correct_parenthesis(instring[last_parenthesis+1:])

def get_third_correct_parenthesis(instring):
    num_parenthesis = 1
    first_parenthesis = instring.find('(')
    if first_parenthesis == -1:
        last_parenthesis = instring.find(')')
        if last_parenthesis != 0:
            return instring[0:last_parenthesis]
        return instring
    last_parenthesis = first_parenthesis
    while num_parenthesis > 0:
        last_parenthesis += 1
        if instring[last_parenthesis] == '(':
            num_parenthesis += 1
        elif instring[last_parenthesis] == ')':
            num_parenthesis -= 1
    return get_second_correct_parenthesis(instring[last_parenthesis+1:])


def clean_mimic_program(mimic_smtfile):
    with open(mimic_smtfile, 'r') as g:
        raw = g.readlines()[1]
    # raw = remove_divisions(raw)
    raw = raw[raw.find("Bool"):]
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
    last_portion = raw[raw.find(let_values[-1])+len(let_values[-1]):]
    for i in range(len(let_values)):
        for j in range(len(let_values)):
            let_values[j] = let_values[j].replace(f"_let_{i+1} ",f"{let_values[i]} ")
            let_values[j] = let_values[j].replace(f"_let_{i+1})",f"{let_values[i]})")

    
    for i in range(len(let_values)):
        last_portion = last_portion.replace(f"_let_{i+1} ",f"{let_values[i]} ")
        last_portion = last_portion.replace(f"_let_{i+1})",f"{let_values[i]})")
    ite = last_portion.find('ite')
    tree_first = get_first_correct_parenthesis(last_portion[ite:])
    tree_second = get_second_correct_parenthesis(last_portion[ite:])
    tree_third = get_third_correct_parenthesis(last_portion[ite:])
    final = f"(ite {tree_first} {tree_second} {tree_third})"
    with open('mnist_mimic_program.txt', 'w') as fp:
        fp.write(final)

def classify_image(pixels):
    file = open("mnist_mimic_program.txt", "r")
    data = file.read()
    file.close()

    data = data.replace("ite", "if")

    args = ""
    size = len(pixels)
    for y in range(size):
        for x in range(size):
            args += "(setv b{}_{} {})".format(y, x, pixels[y][x])

    prog = args + data
    expr = hy.read(f"((fn [] {prog}))")
    return hy.eval(expr)


def createFile(constraints_ind, tempfile):
    # g = open("smtfiles/mnist_myconstrs.txt", "rt")
    g = open("smtfiles/mnist_constraints.smt2", "rt")
    all_constraints = g.readlines()
    g.close()
    # print(constraints)
    f = open(tempfile, 'w')
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
    os.system(f'../cvc5-Linux --lang=sygus2 {tempfile} >mnist_mimic.smt2')

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
    
    # runtime_data.to_csv('mnist_runtime.csv')

def mimic_program_global_accuracy(T):
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    xtotest = x_test.astype("float32") / 255
    ytotest = y_test

    right_predictions = 0
    total_predictions = 0

    for i in tqdm(range(xtotest.shape[0])):
        ground_truth = ytotest[i]
        if ground_truth == 1 or ground_truth == 7:
            total_predictions += 1
            program_outcome = classify_image(list(xtotest[i]))
            if program_outcome == (ground_truth == 1):
                right_predictions += 1
    return right_predictions/total_predictions

    


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
    # num_constraints = 10
    # with open("smtfiles/mnist_constraints.smt2", "rt") as g:
    #     all_constraints = g.readlines()
    # arr_constraints = random.sample(range(0,len(all_constraints)), num_constraints)
    # createFile(arr_constraints)

    ### UNDER CONSTRUCTION
    g = open("smtfiles/mnist_constraints.smt2", "rt")
    all_constraints = g.readlines()
    g.close()
    total_num_constraints = len(all_constraints)-5 # -5 for safety

    T = TrainingInstance(10, (28,28,1))
    T.data_preparation()
    # with open('models/mnist_model.pkl', 'br') as fp:
    #     T.model = pickle.load(fp)
    T.load_model('models/mnist_model.h5')
    constraints = [10, 20, 30, 40, 50, 60, 70, 80]

    global_accuracy = pd.DataFrame(columns=constraints)
    n=10
    for num_constraints in tqdm(constraints):
        for i in tqdm(range(n)):
            tempfile = 'smtfiles/temp_mnist.smt2'
            arr_constraints = random.sample(range(0,total_num_constraints), num_constraints)
            createFile(arr_constraints, tempfile)
            clean_mimic_program('mnist_mimic.smt2')
            global_accuracy.loc[i,num_constraints] = mimic_program_global_accuracy(T)

    global_accuracy.to_csv('data/mnist_global_accuracy.csv')
    
    
if __name__ == "__main__":
    main()
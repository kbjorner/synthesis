import time, os, argparse, random
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc

def make_random_dataset():
    iterate = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    runtime_data = pd.DataFrame(columns=iterate, index=range(1,11))
    for num_constraints in iterate:
        for i in range(1,11):
            runtime_data.loc[i,num_constraints] = random.random()
    return runtime_data


def make_graph(df, benchmark):
    # iterate = np.array(df.columns.astype('int'))
    iterate = df.columns
    means = []
    lowerbound = []
    upperbound = []

    for i in iterate:
        data = df[i]
        mean = data.mean()
        stdev = data.std()
        lowbound = mean - stdev
        upbound = mean + stdev
        means.append(mean)
        lowerbound.append(lowbound)
        upperbound.append(upbound)
    maxtime = max(upperbound)
    
    iterate = np.array(df.columns.astype('int'))
    fontsize = 16
    plt.rcParams.update({'font.size': fontsize})
    rc('font', **{'family': 'serif', 'serif': ['Times']})
    rc('text', usetex=True)

    c = '#ff0000'
    plt.fill_between(iterate, lowerbound, upperbound, color = '#FF9F9F')
    plt.plot(iterate, means, color = c, marker = 'o')
    
    plt.legend(['Mean', 'Mean $\pm$ stdev'])
    plt.xlabel('Number of Constraints', size = fontsize)
    plt.ylabel('Runtime (seconds)', size=fontsize)
    plt.title(f'Mimic Program Synthesis on {benchmark}', size = fontsize + 2)
    
    yspaced = np.linspace(0,maxtime,5)
    ysize = 1000
    while (maxtime/ysize < 10):
        ysize = ysize/10
    ynums = [ysize*int(yspaced[i]/ysize) for i in range(len(yspaced)) ]
    ystrs = [str(ynums[i]) for i in range(len(ynums))]
    plt.yticks(ynums, ystrs)    
    xnums = iterate[::2]
    xstrs = [str(xnums[i]) for i in range(len(xnums))]
    plt.xticks(xnums, xstrs)
    # plt.margins(x = 0)
    plt.savefig(f'{benchmark}_runtime.pdf')
    plt.clf()
    # plt.show()

def main():
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('--host', metavar='H', default='127.0.0.1', help='IP of the host server (default: 127.0.0.1)')
    args = argparser.parse_args()

    paths_to_data = ['mnist.csv', 'pima.csv']
    df = make_random_dataset()
    maxcol = pd.read_csv('../data/mnist_runtime.csv').shape[1]
    df = pd.read_csv('../data/mnist_runtime.csv', usecols=[i for i in range(1,maxcol)])    
    make_graph(df, "MNIST")
    maxcol = pd.read_csv('../data/pima_runtime_anal.csv').shape[1]
    df = pd.read_csv('../data/pima_runtime_anal.csv', usecols=[i for i in range(1,maxcol)])
    make_graph(df, "Pima")



if __name__ == "__main__":
    main()
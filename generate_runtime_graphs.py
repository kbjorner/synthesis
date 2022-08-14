from pickletools import markobject
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


def make_graph(df1, df2, benchmark, plotcolor, fillcolor):
    # iterate = np.array(df.columns.astype('int'))
    iterate = df1.columns
    means = []
    lowerbound = []
    upperbound = []

    means2 = []
    lowerbound2 = []
    upperbound2 = []

    for i in iterate:
        data = df1[i]
        data2 = df2[i]
        mean = data.mean()
        mean2 = data2.mean()
        # mean = data.median()
        stdev = data.std()
        stdev2 = data2.std()
        lowbound = mean - stdev
        lowbound2 = mean2 - stdev2
        # lowbound = data.quantile(0.25)
        upbound = mean + stdev
        upbound2 = mean2 + stdev2
        # upbound = data.quantile(0.75)
        means.append(mean)
        lowerbound.append(lowbound)
        upperbound.append(upbound)
        means2.append(mean2)
        lowerbound2.append(lowbound2)
        upperbound2.append(upbound2)
    maxtime = max(max(upperbound), max(upperbound2))
    

    
    iterate = np.array(df1.columns.astype('int'))
    fontsize = 16
    plt.rcParams.update({'font.size': fontsize})
    rc('font', **{'family': 'serif', 'serif': ['Times']})
    rc('text', usetex=True)

    plt.fill_between(iterate, lowerbound, upperbound, color = fillcolor)
    plt.plot(iterate, means, color = plotcolor, marker = 'o', markersize=4)
    if benchmark == "Pima":
        plt.fill_between(iterate, lowerbound2, upperbound2, color = '#009F9F', alpha = 0.5)
        plt.plot(iterate, means2, color = '#008080', marker = 'o', markersize=4)
    if benchmark == "Pima":
        plt.legend(['Mean Boostrap', 'Mean Simple', 'Mean $\pm$ stdev','Mean $\pm$ stdev'])
    else:
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
    plt.savefig(f'{benchmark}_runtime.pdf', bbox_inches='tight')
    # plt.show()

def main():
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('--host', metavar='H', default='127.0.0.1', help='IP of the host server (default: 127.0.0.1)')
    args = argparser.parse_args()

    plotcolor = '#DC3220'
    fillcolor = '#DC9F9F'

    paths_to_data = ['mnist.csv', 'pima.csv']
    df = make_random_dataset()
    maxcol = pd.read_csv('data/mnist_runtime.csv').shape[1]
    df = pd.read_csv('data/mnist_runtime.csv', usecols=[i for i in range(1,maxcol)])    
    make_graph(df,df, "MNIST", plotcolor=plotcolor, fillcolor=fillcolor)
    plt.clf()
    maxcol = pd.read_csv('data/pima_runtime_bootstrap.csv').shape[1]
    df1 = pd.read_csv('data/pima_runtime_bootstrap.csv', usecols=[i for i in range(1,maxcol)])
    df2 = pd.read_csv('data/pima_runtime_simple.csv', usecols=[i for i in range(1,maxcol)])
    make_graph(df1, df2, "Pima", plotcolor,fillcolor)


if __name__ == "__main__":
    main()
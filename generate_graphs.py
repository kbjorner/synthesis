import argparse, random, csv
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc

plotcolor = '#DC3220'
fillcolor = '#DC9F9F'

def make_random_dataset():
    iterate = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    runtime_data = pd.DataFrame(columns=iterate, index=range(1,11))
    for num_constraints in iterate:
        for i in range(1,11):
            runtime_data.loc[i,num_constraints] = random.random()
    return runtime_data


def make_runtime_graph(df1, df2, benchmark, plotcolor, fillcolor):
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

    fig, ax = plt.subplots()

    plt.fill_between(iterate, lowerbound, upperbound, color = fillcolor)
    plt.plot(iterate, means, color = plotcolor, marker = 'o', markersize=4)
    if benchmark == "Pima":
        plt.fill_between(iterate, lowerbound2, upperbound2, color = '#009F9F', alpha = 0.5)
        plt.plot(iterate, means2, color = '#008080', marker = 'o', markersize=4)
    if benchmark == "Pima":
        plt.legend(['Mean Boostrap', 'Mean Simple', 'Mean $\pm$ stdev','Mean $\pm$ stdev'])
    else:
        plt.legend(['Mean', 'Mean $\pm$ stdev'])

    for spine in ['right', 'top']:
        ax.spines[spine].set_visible(False)
    plt.xlabel('Number of Examples', size = fontsize)
    plt.ylabel('Runtime (seconds)', size=fontsize)
    # plt.title(f'Mimic Program Synthesis on {benchmark}', size = fontsize + 2)
    
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
    if benchmark == "MNIST":
        ax.set_aspect(aspect=0.75)
    # plt.margins(x = 0)
    plt.savefig(f'images/{benchmark}_runtime.pdf', bbox_inches='tight')
    # plt.show()

def make_pima_global_accuracy_graph(grammar_type="bootstrap"):
    accuracy = pd.read_csv(f'data/pima_global_accuracy_{grammar_type}.csv')
    head = accuracy.columns[1:]
    rows = [list(accuracy.loc[0,head].astype(str))]

    recall = pd.read_csv(f'data/pima_global_recall_{grammar_type}.csv')
    head2 = recall.columns[1:]
    rows2 = [list(recall.loc[0,head2].astype(str))]
    plotcolor = '#DC3220'
    horizcolor = '#FF6600'

    # hliney = '' # enter path to this value, replace line below with this.
    hliney = 0.78

#     define vars
    x = []
    y = []
    z = []
    for n in head:
        x.append(int(n))
    for accur in rows[0]:
        y.append(float(accur))
    for rec in rows2[0]:
        z.append(float(rec))
    
    fig, ax = plt.subplots()
    plt.margins(x = 0)
    plt.plot(x, y, color = plotcolor, marker = 'o', markersize=4)
    plt.plot(x,z,color = '#008080', marker = 'o', markersize=4)
    plt.axhline(hliney, color = horizcolor, linestyle = '--')
#     plt.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
    
    for spine in ['right', 'top']:
        ax.spines[spine].set_visible(False)
    
    plt.legend(['Mimic Program Accuracy', 'Mimic Program Recall', 'Opaque Model Accuracy'])
#     plt.title('Comparative Pima Accuracy: Opaque Model vs. Mimic Program')
    plt.xlabel('Number of Examples')
    plt.ylabel('Accuracy (\%)')
    plt.xticks([8, 30, 50, 70, 90, 110, 130], ['10', '30', '50', '70', '90', '110', '130'])
    plt.yticks([0.0, 0.5, 1.0],['0', '50', '100']) # can be commented out to remov whtie space? if desired
    
    plt.savefig(f'images/pima_accuracy_vs_recall_{grammar_type}.pdf', bbox_inches='tight')
    # plt.show()



def readCSVfile_mnist_accuracy(csvfile):
    head = []
    rows = []
    means = []
    lowbound = []
    upbound = []
    
    file = open(csvfile)
    readcsv = csv.reader(file)
    df = pd.read_csv(csvfile)

    
    head = next(readcsv)
    head.pop(0)

    for i, line in enumerate(readcsv):
        rows.append(line)
        rows[i].pop(0)
    rows

    file.close()
    
    for col in head:
        data = 100*df[col]
        mean = data.mean()
        means.append(mean)
        
        stddev = data.std()
        lowbound.append(mean - stddev)
        upbound.append(mean + stddev)
#     print(f"means: {means}; upperbound: {upperbound}")
    return df, head, rows, means, lowbound, upbound


def mnist_accuracy_plot():
    
    plotcolor = '#DC3220'
    fillbetweencolor = '#DC9F9F'
    horizcolor = '#FF6600'

    # hliney = '' # enter path to this value, replace line below with this.
    hliney = 99
    df1, head1, rows1, means1, lowbound1, upbound1 = readCSVfile_mnist_accuracy('data/mnist_global_accuracy.csv')
    df2, head2, rows2, means2, lowbound2, upbound2 = readCSVfile_mnist_accuracy('data/mnist_global_recall.csv')
#     define vars
    x = []
    for n in head1:
        x.append(int(n))

    fig, (ax, ax2) = plt.subplots(2, 1, sharex=True)
    
    
    
    ax.fill_between(x, lowbound1, upbound1, color = fillbetweencolor, alpha = 0.7)
    ax.plot(x, means1, color = plotcolor, marker = 'o', markersize=4)
    ax.fill_between(x, lowbound2, upbound2, color = '#009F9F', alpha = 0.3)
    ax.plot(x, means2, color = '#008080', marker = 'o', markersize=4)
    ax.axhline(hliney, color = horizcolor, linestyle = '--')
    
    ax2.fill_between(x, lowbound1, upbound1, color = fillbetweencolor, alpha = 0.6)
    ax2.plot(x, means1, color = plotcolor, marker = 'o', markersize=4)
    ax2.fill_between(x, lowbound2, upbound2, color = '#009F9F', alpha = 0.4)
    ax2.plot(x, means2, color = '#008080', marker = 'o', markersize=4)
    ax2.axhline(hliney, color = horizcolor, linestyle = '--')
    
    ax.set_ylim(90, 100)
    ax2.set_ylim(50,60)
    
    ax.spines['bottom'].set_visible(False)
    ax2.spines['top'].set_visible(False)
#     ax.xaxis.tick_top()
    ax.axes.xaxis.set_visible(False)
    ax.tick_params(labeltop=False)  # don't put tick labels at the top
    ax2.xaxis.tick_bottom()
    
    d = .015  # how big to make the diagonal lines in axes coordinates
    # arguments to pass to plot, just so we don't keep repeating them
    kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
    ax.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
#     ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

    kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
    ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
#     ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal
    
    
    
    for spine in ['right', 'top']:
        ax.spines[spine].set_visible(False)
        ax2.spines[spine].set_visible(False)
    
    fig.legend(['Mimic Program Accuracy','Mimic Program Recall', 'Opaque Model Accuracy'], loc=[0.4,0.6])
#     plt.title('Comparative MNIST Accuracy: Opaque Model vs. Mimic Program')
    plt.xlabel('Number of Examples')
    plt.ylabel('Accuracy (\%)')
#     plt.yticks([0.0, 0.5, 1.0],['', '0.5', '1.0']) # can be commented out to remov whtie space? if desired
    
    plt.savefig('images/mnist_accuracy_vs_recall.pdf')
    # plt.show()

def pima_runtime_graph():
    plt.clf()
    maxcol = pd.read_csv('data/pima_runtime_bootstrap.csv').shape[1]
    df1 = pd.read_csv('data/pima_runtime_bootstrap.csv', usecols=[i for i in range(1,maxcol)])
    df2 = pd.read_csv('data/pima_runtime_simple.csv', usecols=[i for i in range(1,maxcol)])
    make_runtime_graph(df1, df2, "Pima", plotcolor,fillcolor)


def mnist_runtime_graph():
    plt.clf()
    df = make_random_dataset()
    maxcol = pd.read_csv('data/mnist_runtime.csv').shape[1]
    df = pd.read_csv('data/mnist_runtime.csv', usecols=[i for i in range(1,maxcol)])    
    make_runtime_graph(df,df, "MNIST", plotcolor=plotcolor, fillcolor=fillcolor)
    

def main():
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('--host', metavar='H', default='127.0.0.1', help='IP of the host server (default: 127.0.0.1)')
    args = argparser.parse_args()
    
    mnist_runtime_graph()
    plt.clf()
    pima_runtime_graph()
    plt.clf()
    mnist_accuracy_plot()
    plt.clf()

    make_pima_global_accuracy_graph(grammar_type="bootstrap")
    plt.clf()
    make_pima_global_accuracy_graph(grammar_type="simple")



if __name__ == "__main__":
    main()
# Synthesizing Mimic Programs - Code & Data Appendix


## Set Up
 
This project has been developed with Python 3.8.10. 
In general, everything should run with Python >= 3.6
and the corresponding dependencies.

To install python dependencies:
```
pip3 install -r requirements.txt
```

To generate mimic programs we rely on cvc5.
On Linux:
```
cd ..
wget https://github.com/cvc5/cvc5/releases/latest/download/cvc5-Linux
sudo chmod +x cvc5-Linux
```
For other systems, go to the [Downloads](https://cvc5.github.io/downloads.html)
and follow installation instructions.

Inside the python scripts, cvc5 is called from an installed binary. To use them, put the path to your binary in the `config.yml` file.


## Project Structure

In general, for each of the usecases, MNIST and Pima, 
there is a "NN" script to train the models, 
a "runtimeExperiments" script, used to make the runtime experiments, 
and a "validation" script, 
used to run the accuracy and recall experiments.

- **data/**: Contains the data that we used and produced. MNIST dataset is not included because it's downloaded directly from Keras.
    - *mnist_global_accuracy.csv*: 
    - *mnist_global_recall.csv*:
    - *mnist_runtime.csv*:
    - *pima_global_accuracy_bootstrap.csv*: 
    - *pima_global_accuracy_quantiles.csv*:
    - *pima_global_recall_bootsrap.csv*:
    - *pima_global_recall_quantiles.csv*:
    - *pima_indians_diabetes.csv*: Contains the Pima dataset
    - *pima_runtime.csv*: Contains the data corresponding to runtime experiments in the Pima benchmark.
- **images/**: Graphs generated go to this folder.
- **models/**: Contains the trained Neural Networks used as opaque models in our evaluation as Keras ready-to-load models.
- **smtfiles/**: Contains the relevant SMT-LIBv2 files. --> To Do: pass them to smt extension
    - *mnist_constraints.smt2*: 
    - *mnist_grammar.smt2*: 
    - *pima_constraints.smt2*: 
    - *pima_grammar_bootstrap.smt2*:
    - *pima_grammar_simple.smt2*:
    - *pima_grammar_template.smt2*:
- **Utilities/**: Miscelaneous utils for visualization.

- **generate_runtime_graphs.py**. Reads data in the `data/` folder and generates all the graphs shown in the paper.
- **mnist_NN.py**: Trains the Neural Network (opaque model) for the MNIST benchmark.
- **mnist_runtime.py**: Makes runtime experiments for MNIST.
- **mnist_validation.py**: Accuracy and recall experiments for the MNIST benchmark.
- **pima_NN.py**: Trains the Neural Network (opaque model) for the Pima benchmark.
- **pima_runtime.py**: Makes runtime experiments for Pima.
- **pima_validation.py**: Accuracy and recall experiments for the Pima benchmark.
- **README.md**: This ReadMe.


## Instructions to reproduce the experiments

### Graphs
To generate all the graphs from the data in the `data/` folder:
```
python3 generate_graphs.py
```

### **MNIST**
First of all, a model needs to be trained
```
python3 mnist_NN.py
```

This will save the corresponding model in the *models/* folder, 
and generate the *smtfiles/mnist_constraints.stm2* file, 
containing the examples for our Programming-by-example method, 
enconded as constraints for the synthesis step later.
This should take about 2 min on a regular laptop.

To run the accuracy and recall experiments:
```
python3 mnist_validation.py
```

This will generate the files *data/mnist_global_accuracy.csv* and *data/mnist_global_recall.csv*, as well as the comparisson plot between them.
This validation is compute intensive, it can take several hours.

For the runtime benchmark:
```
python3 mnist_runtime.py
```


### **Pima**
First of all, a model needs to be trained
```
python3 pima_Pima.py
```

This will save the corresponding model in the *models/* folder, 
and generate the constraints file file, 
containing the examples for our Programming-by-example method, 
enconded as constraints for the synthesis step later.
In the case of Pima, the constraints are sorted by acending *confidence*, 
so that *harder* examples are used to make the mimic programs.
This should take less than 1 min on a regular laptop.

To run the accuracy and recall experiments:
```
python3 pima_validation.py
```

This will generate the files *data/pima_global_accuracy_bootstrap.csv*, *data/pima_global_accuracy_simple.csv*,  and *data/pima_global_recall_bootstrap.csv*, *data/pima_gloal_recall_simple.csv*, as well as the comparisson plot between them.

For the runtime benchmark:
```
python3 pima_runtime.py
```

# Synthesizing Local Mimic Programs for Opaque Models - Code & Data Appendix

This repository is the accompaning repository for the paper **Synthesizing Local Mimic Programs for Opaque Models** submitted to AAAI 23.


## Set Up
 
To do


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
    - *pima_runtime.csv*: Contains the data corresponding to runtime experiments in the Pima benchmark. --> ToDo: mix this runtimebootstrap.
- **images/**: Contains the graphs generated.
- **models/**: Contains the trained Neural Networks used as opaque models in our evaluation as Keras ready-to-load models.
- **smtfiles/**: Contains the relevant SMT-LIBv2 files. --> To Do: pass them to smt extension
    - *mnist_constraints.smt2*: 
    - *mnist_grammar.smt2*: 
    - *pima_constraints.smt2*: 
    - *pima_grammar_bootstrap.smt2*:
    - *pima_grammar_quantiles.smt2*:
- **Utilities/**: Miscelaneous utils for visualization.

- **generate_runtime_graphs.py**. This script reads data in the `data/` folder and generates all the graphs shown in the paper.
- **mnist_NN.py**: Trains the Neural Network (opaque model) for the MNIST benchmark.
- **mnist_runtime.py**: Makes runtime experiments for MNIST.
- **mnist_validation.py**: ...
- **pima_NN.py**: Trains the Neural Network (opaque model) for the Pima benchmark.
- **pima_runtime.py**: Makes runtime experiments for Pima.
- **pima_validation.py**: ...
- **README.md**: This ReadMe.


## Instructions to reproduce the experiments





## MNIST

## Pima





# Todolist for getting presentable repository
- Make a data/ folder, where all our runtime, models and training data is stored.
- Make a script to generate MNIST grammar
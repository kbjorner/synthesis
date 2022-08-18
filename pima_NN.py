from random import random
import numpy as np
import pandas as pd
from tensorflow import keras
import tensorflow as tf
from datetime import datetime
import os
from collections import Counter
from sklearn import tree
import graphviz, pickle


"""
Class to train and evaluate MNIST dataset. Saves model.
Saves generated constraints.
"""


class TrainingInstance:
    def __init__(self):
        self.features = [ 
            'Pregnancies', 
            'Glucose', 
            'BloodPressure', 
            'SkinThickness', 
            'Insulin', 
            'BMI', 
            'DiabetesPedigreeFunction', 
            'Age', 
            'Outcome' 
        ]

        self.data = pd.read_csv('data/pima_indians_diabetes.csv', names= self.features)
        # (self.x_train, self.y_train), (self.x_test, self.y_test) = keras.datasets.mnist.load_data()
        self.timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.save_model = f"models/pima_model_{self.timestamp}.h5"

    def data_preparation(self):
        for col in self.data:
            self.data[ col ] = self.data[ col ].astype( float )
        # fill NaNs with mean value
        for col in [ 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI' ]:
            mean = self.data[ self.data[ col ] != 0.0 ][ col ].mean()
            self.data[ col ] = self.data[ col ].replace( 0.0, mean )
        
        # shuffle data "in place": https://stackoverflow.com/a/34879805
        # with random state for consistency for the train/test split
        self.data = self.data.sample( frac = 1 , random_state=42).reset_index( drop = True )

        xs = self.data.copy()
        ys = xs.pop( 'Outcome' ).to_frame( name = 'Outcome' )

        test_len = len( xs ) // 5

        self.train_xs, self.test_xs = xs.head( len( xs ) - test_len ), xs.tail( test_len )
        self.train_ys, self.test_ys = ys.head( len( xs ) - test_len ), ys.tail( test_len )

    def load_model(self, model_path):
        print(model_path)
        self.model = keras.models.load_model(model_path)

    def build_model(self):
        norm = keras.layers.Normalization()
        norm.adapt( self.train_xs )
        self.model = keras.Sequential()
        self.model.add( norm )
        self.model.add( keras.layers.Dense( 9, input_dim=9, kernel_initializer='normal', activation='relu' ) )
        self.model.add( keras.layers.Dense( 20, activation='relu' ) )
        self.model.add( keras.layers.Dense( 20, activation='relu' ) )
        self.model.add( keras.layers.Dense( 1, activation='relu' ) )
        self.model.add( keras.layers.ReLU( max_value = 1.0 ) ) # for clamping
        self.model.summary()
    
    def train_model(self):
        self.model.compile( loss = tf.losses.MeanSquaredError(), optimizer = "adam", metrics=[ tf.keras.metrics.MeanSquaredError()] )
        self.model.compile( loss = tf.losses.MeanSquaredError(), optimizer = "adam", metrics=[ "accuracy"] )
        self.model.fit( self.train_xs, self.train_ys, epochs = 30 )
        # self.model.save(self.save_model)
        with open(f'models/pima_model_{self.timestamp}.pkl', 'bw') as fp:
            pickle.dump(self.model, fp)


    def evaluate_model(self):
        score = self.model.evaluate(self.test_xs, self.test_ys, verbose=0)
        print("Test loss:", score[0])
        print("Test accuracy:", score[1])

    def make_constraints(self):
        f = open("smtfiles/pima_constraints.txt", "w")
        oneCounter = 0
        zeroCounter = 0
        
        outcomes = self.model.predict([self.test_xs.values]).reshape(len(self.test_xs.values),)
        outcomes_df = pd.DataFrame(columns=['outcome', 'confidence', 'prediction'])
        outcomes_df.outcome = outcomes
        outcomes_df.prediction = outcomes_df.outcome > 0.5
        outcomes_df.confidence = np.abs(outcomes - 0.5)
        outcomes_df = outcomes_df.sort_values('confidence') # sorted, lowest confidence first

        for i in outcomes_df.index:
            point = self.test_xs.values[i]
            # outcome = self.test_ys.values[i]  # for ground truth
            outcome = outcomes_df.loc[i,'prediction']
            f.write("(constraint (= (rig_mimic {}) {}))\n".format(' '.join(map(lambda x: "{:.4f}".format(x), point)), 'true' if outcome else 'false'))
            if outcome:
                oneCounter += 1
            else:
                zeroCounter += 1

        self.outcomes_df = outcomes_df


        f.close()

        print(f"ones: {oneCounter}; zeros: {zeroCounter}")

    def local_accuracy(self, index_array):
        xtotest = self.test_xs.reset_index(drop=True)[self.test_xs.reset_index(drop=True).index.isin(index_array)]
        ytotest = self.test_ys.reset_index(drop=True)[self.test_ys.reset_index(drop=True).index.isin(index_array)]
        score = self.model.evaluate(xtotest, ytotest, verbose=0)
        return score[1]

    def computeMagicNumbers(self):
        X, Y = self.test_xs.to_numpy(), self.test_ys.to_numpy()
        var_names, class_name  = list(self.test_xs.columns), list(self.test_ys.columns)

        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(X, Y)
        features = clf.tree_.feature
        threshold = clf.tree_.threshold

        # print(f"feature: {features}")
        # print(f"threshold: {threshold}")

        bootstrap_numbers = [[] for i in range(max(features) +1)]
        for i, feature in enumerate(features):

            if feature >= 0:
                bootstrap_numbers[features[i]].append(threshold[i])

        simple_numbers = [[] for i in range(len(self.data.columns[:-1]))]
        for i in range(len(self.data.columns[:-1])):
            col = self.data.columns[i]
            q1 = self.data[col].quantile(0.25)
            q2 = self.data[col].quantile(0.5)
            q3 = self.data[col].quantile(0.75)
            simple_numbers[i] = [q1, q2, q3]
        
        with open('smtfiles/pima_grammar_template.txt', 'r') as fp:
            grammar_template =fp.read()

        codenames = {
            "Pregnancies" : "P",
            "Glucose" : "G",
            "BloodPressure": "BP",
            "SkinThickness" : "ST",
            "Insulin": "I",
            "BMI" : "BMI",
            "DiabetesPedigreeFunction" : "DPF",
            "Age" : "A"
        }

        grammarstr = grammar_template
        for feature in codenames.keys():
            magic_numbers_str = " ".join([str(i) for i in bootstrap_numbers[var_names.index(feature)]])
            if len(bootstrap_numbers[var_names.index(feature)]) == 0:
                magic_numbers_str = simple_numbers[var_names.index(feature)][1] # use q2 if no number in feature
                # print(f"It happened! with {var_names.index(feature)}, {feature} \n")
            grammarstr = grammarstr.replace(f"({codenames[feature]} Real ()", f"({codenames[feature]} Real ({magic_numbers_str})")

        with open('smtfiles/pima_grammar_bootstrap.smt2', 'w') as fp:
            fp.write(grammarstr)

        grammarstr = grammar_template
        for feature in codenames.keys():
            magic_numbers_str = " ".join([str(i) for i in simple_numbers[var_names.index(feature)]])
            grammarstr = grammarstr.replace(f"({codenames[feature]} Real ()", f"({codenames[feature]} Real ({magic_numbers_str})")

        with open('smtfiles/pima_grammar_simple.smt2', 'w') as fp:
            fp.write(grammarstr)

        # for i in range(8):
        #     print(f"{var_names[i]}: {bootstrap_numbers[i]}" )


def main():
    T = TrainingInstance()
    T.data_preparation()
    T.build_model()
    T.train_model()
    T.evaluate_model()
    T.make_constraints()
    T.computeMagicNumbers()


if __name__ == "__main__":
    main()
import numpy as np
import pandas as pd
from tensorflow import keras
import tensorflow as tf
from datetime import datetime
import math
from collections import Counter


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

        self.data = pd.read_csv('data/diabetes.csv', names= self.features)
        # (self.x_train, self.y_train), (self.x_test, self.y_test) = keras.datasets.mnist.load_data()
        self.timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.save_model = f"pima_model_{self.timestamp}.h5"

    def data_preparation(self):
        for col in self.data:
            self.data[ col ] = self.data[ col ].astype( float )
        # fill NaNs with mean value
        for col in [ 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI' ]:
            mean = self.data[ self.data[ col ] != 0.0 ][ col ].mean()
            self.data[ col ] = self.data[ col ].replace( 0.0, mean )
        
        # shuffle data "in place": https://stackoverflow.com/a/34879805
        self.data = self.data.sample( frac = 1 ).reset_index( drop = True )

        xs = self.data.copy()
        ys = xs.pop( 'Outcome' ).to_frame( name = 'Outcome' )

        test_len = len( xs ) // 5

        self.train_xs, self.test_xs = xs.head( len( xs ) - test_len ), xs.tail( test_len )
        self.train_ys, self.test_ys = ys.head( len( xs ) - test_len ), ys.tail( test_len )

        

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
        self.model.fit( self.train_xs, self.train_ys, epochs = 20 )
        self.model.save(self.save_model)

    def evaluate_model(self):
        score = self.model.evaluate(self.test_xs, self.test_ys, verbose=0)
        print("Test loss:", score[0])
        print("Test accuracy:", score[1])

    def make_constraints(self):
        f = open("smtfiles/pima_constraints.txt", "w")
        n = 100
        oneCounter = 0
        zeroCounter = 0
        for i in range(len(self.test_xs)):
            point = self.test_xs.values[i]
            outcome = self.test_ys.values[i]  # for ground truth
            outcome = self.model.predict([self.test_xs.values[i]])[0,0]  # for predictions --> make more efficient
            # outcome = 1 if outcome > 0.5 else 0
            if outcome > 0.5:
                outcome = 1
            else:
                outcome = 0
            f.write("(constraint (= (rig_mimic {}) {}))\n".format(' '.join(map(lambda x: "{:.4f}".format(x), point)), 'true' if outcome == 1 else 'false'))
            if outcome == 1:
                oneCounter += 1
            else:
                zeroCounter += 1

        f.close()

        print(f"ones: {oneCounter}; zeros: {zeroCounter}")

def main():
    T = TrainingInstance()
    print(T.data)
    T.data_preparation()
    T.build_model()
    T.train_model()
    T.evaluate_model()
    T.make_constraints()



if __name__ == "__main__":
    main()
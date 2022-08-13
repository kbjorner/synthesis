import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from datetime import datetime
import math
from collections import Counter


"""
Class to train and evaluate MNIST dataset. Saves model.
"""


class TrainingInstance:
    def __init__(self, num_classes, input_shape):
        self.num_classes = num_classes
        self.input_shape = input_shape
        # the data, split between train and test sets
        (self.x_train, self.y_train), (self.x_test, self.y_test) = keras.datasets.mnist.load_data()
        self.timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.save_model = f"my_model_{self.timestamp}.h5"

    def display_digit(self, img):
        for row in img:
            for pix in row:
                print('X' if pix > 0 else ' ', end='')
            print('')

    def get_truth(self, arr):
        for i, value in enumerate(arr):
            if value > 0:
                return i
        return -1

    def get_prediction(self, arr):
        max_digit = 0
        for i, value in enumerate(arr):
            if arr[max_digit] < value:
                max_digit = i
        return max_digit

    def distance(self,arr1, arr2):
        return math.sqrt(sum([pow(arr1[i] - arr2[i], 2) for i in range(len(arr1))]))


    def data_preparation(self):
        # Scale images to the [0, 1] range
        self.x_train = self.x_train.astype("float32") / 255
        self.x_test = self.x_test.astype("float32") / 255
        # Make sure images have shape (28, 28, 1)
        self.x_train = np.expand_dims(self.x_train, -1)
        self.x_test = np.expand_dims(self.x_test, -1)

        # convert class vectors to binary class matrices
        self.y_train = keras.utils.to_categorical(self.y_train, self.num_classes)
        self.y_test = keras.utils.to_categorical(self.y_test, self.num_classes)

        print("x_train shape:", self.x_train.shape)
        print(self.x_train.shape[0], "train samples")
        print(self.x_test.shape[0], "test samples")

    def build_model(self):
        self.model = keras.Sequential(
            [
                keras.Input(shape=self.input_shape),
                layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
                layers.MaxPooling2D(pool_size=(2, 2)),
                layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
                layers.MaxPooling2D(pool_size=(2, 2)),
                layers.Flatten(),
                layers.Dropout(0.5),
                layers.Dense(self.num_classes, activation="softmax"),
            ]
        )

    def train_model(self, batch_size, epochs, save=True):
        self.model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
        self.model.fit(self.x_train, self.y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)
        if save:
            self.model.save(self.save_model)

    def simple_evaluation(self):
        score = self.model.evaluate(self.x_test, self.y_test, verbose=0)
        print("Test loss:", score[0])
        print("Test accuracy:", score[1])

    def evaluate_model(self):
        # The ground truth value (which digit) associated with each test case
        ground_truth = [self.get_truth(y) for y in self.y_test]        
        # The number of times each digit appears in the tests (worth noting that each
        # digit does not occur the same number of times)
        test_occur = Counter(ground_truth)

        # The outputs of the model for each test case
        predictions = self.model.predict(self.x_test)
        # The accuracy of the model's predictions (lower score is better)
        scores = [self.distance(predictions[i], self.y_test[i]) for i in range(len(predictions))]
        # The indicies of the "predictions" array sorted in descending order by score
        # The ones that come first point to tests for which the model was least accurate
        offending_inds = list(reversed(sorted([i for i in range(len(predictions))], key=lambda x: scores[x])))
        # The "hardest" tests mapped to their ground truth values
        offending_digits = list(map(lambda x: ground_truth[x], offending_inds))

        # The average score for each digit, 0-9 (lower is better)
        # avg_scores = {1: 0, 7: 0}
        avg_scores = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
        print(len(offending_digits), len(offending_inds))
        for ind in offending_inds:
            print(ind)
            avg_scores[offending_digits[ind]] += scores[ind]
        for key in avg_scores:
            avg_scores[key] /= test_occur[key]

        ranked_digits = reversed(sorted(avg_scores.keys(), key=lambda x: avg_scores[x]))
        print("Average score for each digit:")
        print("(lower is better)".center(29))
        print("=============================")

        for digit in ranked_digits:
            print("{}:  {}".format(digit, round(avg_scores[digit], 5)).center(29))
        print('')

        num_challenging = 3
        print(f"The first {num_challenging} most challenging test cases:")
        print("==========================================")

        for ind in offending_inds[:num_challenging]:
            print("Digit: {}".format(ground_truth[ind]))
            print("Prediction: {}".format(self.get_prediction(predictions[ind])))
            print("Score: {}".format(round(scores[ind], 5)))
            print("Index: x_test[{}]".format(ind))
            self.display_digit(self.x_test[ind])
    
    def load_model(self, model_path):
        self.model = keras.models.load_model(model_path)


def main():
    T = TrainingInstance(10, (28,28,1))
    T.data_preparation()
    # T.display_digit(T.x_train[20])
    # print(T.y_train[20])
    T.build_model()
    print(T.model.summary())

    batch_size = 4 # Normally 128
    epochs = 1 # Normally 15
    # T.train_model(batch_size=batch_size, epochs=epochs)
    T.load_model("my_model_2022-08-13T19:55:30.h5")
    # T.evaluate_model()
    T.simple_evaluation()


if __name__ == "__main__":
    main()
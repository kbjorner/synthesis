import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from datetime import datetime
import math
from collections import Counter


"""
Class to train and evaluate MNIST dataset. Saves model.
Saves generated constraints.
"""


class TrainingInstance:
    def __init__(self, num_classes, input_shape):
        self.num_classes = num_classes
        self.input_shape = input_shape
        # the data, split between train and test sets
        (self.x_train, self.y_train), (self.x_test,
                                       self.y_test) = keras.datasets.mnist.load_data()
        self.timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.save_model = f"mnist_model_{self.timestamp}.h5"

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

    def distance(self, arr1, arr2):
        return math.sqrt(sum([pow(arr1[i] - arr2[i], 2) for i in range(len(arr1))]))

    # Identify test cases close to decision boundaries
    def get_choices(self, pred):
        highest_inds = sorted(
            [i for i in range(len(pred))], key=lambda x: pred[x])
        return list(reversed(highest_inds[-2:]))

    def get_indecision(self, pred):
        highest = sorted(pred)[-2:]
        return highest[1] - highest[0]

    def data_preparation(self):
        # Scale images to the [0, 1] range
        self.x_train = self.x_train.astype("float32") / 255
        self.x_test = self.x_test.astype("float32") / 255
        # Make sure images have shape (28, 28, 1)
        self.x_train = np.expand_dims(self.x_train, -1)
        self.x_test = np.expand_dims(self.x_test, -1)

        # convert class vectors to binary class matrices
        self.y_train = keras.utils.to_categorical(
            self.y_train, self.num_classes)
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

    def train_model(self, batch_size, epochs, save=False):
        self.model.compile(loss="categorical_crossentropy",
                           optimizer="adam", metrics=["accuracy"])
        self.model.fit(self.x_train, self.y_train,
                       batch_size=batch_size, epochs=epochs, validation_split=0.1)
        if save:
            self.model.save(self.save_model)

    def simple_evaluation(self):
        score = self.model.evaluate(self.x_test, self.y_test, verbose=0)
        print("Test loss:", score[0])
        print("Test accuracy:", score[1])

    def evaluate_model(self, verbose=0):
        # The ground truth value (which digit) associated with each test case
        ground_truth = [self.get_truth(y) for y in self.y_test]
        # The number of times each digit appears in the tests (worth noting that each
        # digit does not occur the same number of times)
        test_occur = Counter(ground_truth)

        # The outputs of the model for each test case
        self.predictions = self.model.predict(self.x_test)
        # The accuracy of the model's predictions (lower score is better)
        scores = [self.distance(self.predictions[i], self.y_test[i])
                  for i in range(len(self.predictions))]
        # The indicies of the "predictions" array sorted in descending order by score
        # The ones that come first point to tests for which the model was least accurate
        offending_inds = list(reversed(
            sorted([i for i in range(len(self.predictions))], key=lambda x: scores[x])))
        # The "hardest" tests mapped to their ground truth values
        offending_digits = list(map(lambda x: ground_truth[x], offending_inds))

        # The average score for each digit, 0-9 (lower is better)
        # avg_scores = {1: 0, 7: 0}
        avg_scores = {0: 0, 1: 0, 2: 0, 3: 0,
                      4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
        for ind in offending_inds:
            avg_scores[offending_digits[ind]] += scores[ind]
        for key in avg_scores:
            avg_scores[key] /= test_occur[key]

        ranked_digits = reversed(
            sorted(avg_scores.keys(), key=lambda x: avg_scores[x]))
        print("Average score for each digit:")
        print("(lower is better)".center(29))
        print("=============================")

        for digit in ranked_digits:
            print("{}:  {}".format(digit, round(
                avg_scores[digit], 5)).center(29))
        print('')

        if verbose > 0:
            num_challenging = 3
            print(f"The first {num_challenging} most challenging test cases:")
            print("==========================================")

            for ind in offending_inds[:num_challenging]:
                print("Digit: {}".format(ground_truth[ind]))
                print("Prediction: {}".format(
                    self.get_prediction(self.predictions[ind])))
                print("Score: {}".format(round(scores[ind], 5)))
                print("Index: x_test[{}]".format(ind))
                self.display_digit(self.x_test[ind])

    def load_model(self, model_path):
        self.model = keras.models.load_model(model_path)

    def make_constraints(self, y0, y1, y2, constraints_file="allConstraints.txt"):
        counter = 0
        g = open(constraints_file, "w")
        for ind in range(len(self.predictions)):
            digit = self.x_test[ind]
            # for when we need ground truth values
            # truth = ground_truth[ind]
            truth = self.get_choices(self.predictions[ind])[0]
            if truth in {y0, y1, y2}:
                # g.write("(constraint (= (rig_mimic {}) {}))\n".format(' '.join(map(
                #     lambda x: "{:.4f}".format(x), digit.flatten())), 'true' if truth == 7 else 'false'))
                if truth == 7:
                    g.write("(constraint (= (rig_mimic {}) 2))\n".format(
                        ' '.join(map(lambda x: "{:.4f}".format(x), digit.flatten()))))
                elif truth == 1:
                    g.write("(constraint (= (rig_mimic {}) 1))\n".format(
                        ' '.join(map(lambda x: "{:.4f}".format(x), digit.flatten()))))
                else:
                    g.write("(constraint (= (rig_mimic {}) 0))\n".format(
                        ' '.join(map(lambda x: "{:.4f}".format(x), digit.flatten()))))

                counter += 1
        g.close()

        print(f"Found {counter} constraints")


def main():
    T = TrainingInstance(10, (28, 28, 1))
    T.data_preparation()
    # T.display_digit(T.x_train[20])
    # print(T.y_train[20])
    T.build_model()
    print(T.model.summary())

    batch_size = 128  # Normally 128
    epochs = 15  # Normally 15
    T.train_model(batch_size=batch_size, epochs=epochs)
    # T.load_model('models/mnist_model.h5')
    T.evaluate_model()
    T.simple_evaluation()
    T.make_constraints(0, 1, 7, f'mnist_constraints_multi.smt2')


if __name__ == "__main__":
    main()

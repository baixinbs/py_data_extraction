import joblib
import numpy as np
import nltk
from keras.models import Sequential, load_model, Model, K
from keras.layers import Dense, Dropout, LSTM, Input, Flatten, Permute, Reshape, Lambda, RepeatVector, Multiply
from dao.new_file_dao import NewFileDao

# from keras.callbacks import ModelCheckpoint
# from keras.utils import np_utils

from resources.file_paths import *


def attention_3d_block(inputs, time_steps, single_attention_vector=True):
    # inputs.shape = (batch_size, time_steps, input_dim)
    input_dim = int(inputs.shape[2])
    a = Permute((2, 1))(inputs)
    a = Reshape((input_dim, time_steps))(a)  # this line is not useful. It's just to know which dimension is what.
    a = Dense(time_steps, activation='softmax')(a)
    if single_attention_vector:
        a = Lambda(lambda x: K.mean(x, axis=1), name='dim_reduction')(a)
        a = RepeatVector(input_dim)(a)
    a_probs = Permute((2, 1), name='attention_vec')(a)
    output_attention_mul = Multiply()([inputs, a_probs])
    return output_attention_mul


class Algorithm(object):
    def __init__(self):
        self.load_x_y()

    def load_x_y(self):
        with open(x_y_file, 'rb') as f:
            x = joblib.load(f)
            y = joblib.load(f)
        print(x.shape)
        print(y.shape)
        x = x.reshape(x.shape[0], x.shape[1], x.shape[2] * x.shape[3])

        train_len = int(len(x) * 0.8)
        self.x_train = x[:train_len]
        self.x_test = x[train_len:]
        self.y_train = y[:train_len]
        self.y_test = y[train_len:]

    def attention_lstm_train(self):
        x_train = self.x_train
        y_train = self.y_train

        input = Input(shape=(x_train.shape[1], x_train.shape[2],))
        attention_mul = attention_3d_block(input, x_train.shape[1])
        lstm = LSTM(50, return_sequences=True)(attention_mul)
        # dropout = Dropout(0.02)(lstm)
        lstm = LSTM(50, return_sequences=True)(lstm)
        # dropout = Dropout(0.02)(lstm)
        lstm = LSTM(50, return_sequences=True)(lstm)
        # dropout = Dropout(0.02)(lstm)
        flatten = Flatten()(lstm)
        output = Dense(2, activation='relu')(flatten)
        model = Model(input=input, output=output)
        model.summary()

        model.compile(optimizer='adam', loss='mean_squared_error')

        batch_size = 128  # Batch size for training.
        epochs = 15  # Number of epochs to train for.
        history = model.fit(x_train, y_train,
                            batch_size=batch_size,
                            epochs=epochs,
                            validation_split=0.2)
        model.save(model_path)

    def evaluate(self):
        model = load_model(model_path)
        score = model.evaluate(self.x_test, self.y_test)
        print("%s: %.2f" % (model.metrics_names, score))

if __name__ == '__main__':
    alg = Algorithm()
    alg.attention_lstm_train()
    alg.evaluate()

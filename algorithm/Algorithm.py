import pickle
import numpy as np
from keras.models import Sequential, load_model, Model, K
from keras.layers import Dense, Dropout, LSTM, Input, Flatten, Permute, Reshape, Lambda, RepeatVector, Multiply


# from keras.callbacks import ModelCheckpoint
# from keras.utils import np_utils


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
        pass

    def lstm_with_y(self):
        with open('E:\\data_extraction_forZhaoDanNing\\data\\pickle\\x_y', 'rb') as f:
            x = pickle.load(f)
            y = pickle.load(f)
            y_location = pickle.load(f)
        print(x.shape)
        print(y.shape)
        print(y_location.shape)
        x = x.reshape(x.shape[0], x.shape[1], x.shape[2] * x.shape[3])
        print(x.shape)

        input = Input(shape=(x.shape[1], x.shape[2],))
        out = LSTM(3, return_sequences=True)(input)

        model = Model(inputs=input, outputs=out)
        model.compile(optimizer='adam', loss='categorical_crossentropy')

        batch_size = 64  # Batch size for training.
        epochs = 10  # Number of epochs to train for.
        model.fit(x, y,
                  batch_size=batch_size,
                  epochs=epochs,
                  validation_split=0.2)

    def lstm_with_y_location(self):
        with open('E:\\data_extraction_forZhaoDanNing\\data\\pickle\\x_y', 'rb') as f:
            x = pickle.load(f)
            y = pickle.load(f)
            y_location = pickle.load(f)
        print(x.shape)
        print(y_location.shape)
        x = x.reshape(x.shape[0], x.shape[1], x.shape[2] * x.shape[3])
        print(x.shape)

        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(x.shape[1], x.shape[2])))
        model.add(Dropout(0.02))
        model.add(LSTM(50, return_sequences=True))
        model.add(LSTM(3, return_sequences=True))
        # model.add(Dropout(0.02))
        model.add(Flatten())
        model.add(Dense(2, activation='relu'))
        model.summary()

        # input = Input(shape=(x.shape[1], x.shape[2], ))
        # out0 = LSTM(20, return_sequences=True)(input)
        # out1 = LSTM(3, return_sequences=True)(out0)
        # out2 = Flatten()(out1)
        # out3 = Dense(2, activation='relu')(out2)
        # model = Model(inputs=input, outputs=out3)
        # model.summary()

        model.compile(optimizer='adam', loss='mean_squared_error')

        batch_size = 256  # Batch size for training.
        epochs = 30  # Number of epochs to train for.
        model.fit(x, y_location,
                  batch_size=batch_size,
                  epochs=epochs,
                  validation_split=0.2)

    def attention_with_y_location(self):
        with open('E:\\data_extraction_forZhaoDanNing\\data\\pickle\\x_y', 'rb') as f:
            x = pickle.load(f)
            y = pickle.load(f)
            y_location = pickle.load(f)
        print(x.shape)
        print(y_location.shape)
        x = x.reshape(x.shape[0], x.shape[1], x.shape[2] * x.shape[3])
        print(x.shape)

        input = Input(shape=(x.shape[1], x.shape[2], ))
        attention_mul = attention_3d_block(input, x.shape[1])
        lstm1 = LSTM(50, return_sequences=True)(attention_mul)
        dropout1 = Dropout(0.02)(lstm1)
        lstm2 = LSTM(50, return_sequences=True)(dropout1)
        lstm3 = LSTM(3, return_sequences=True)(lstm2)
        flatten1 = Flatten()(lstm3)
        output = Dense(2, activation='relu')(flatten1)
        model = Model(input=input, output=output)
        model.summary()

        model.compile(optimizer='adam', loss='mean_squared_error')

        batch_size = 256  # Batch size for training.
        epochs = 30  # Number of epochs to train for.
        model.fit(x, y_location,
                  batch_size=batch_size,
                  epochs=epochs,
                  validation_split=0.2)


if __name__ == '__main__':
    alg = Algorithm()
    # alg.lstm_with_y()
    # alg.lstm_with_y_location()
    alg.attention_with_y_location()

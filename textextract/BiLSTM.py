import pandas as pd
import gensim
import gensim
import numpy as np
import tensorflow as tf
from tensorflow.keras import models, layers, optimizers, losses, metrics


class bilstm(models.Model):
    def __init__(self, input_shape, w2v_filename='./Data/wiki.zh.text.vector',vector_dim=400, hidden_size=256, wv_trainable=False):
        super(bilstm, self).__init__()
        self.vector_dim = vector_dim
        self.wv_trainable = wv_trainable
        self.hidden_size = hidden_size
        word2vec = gensim.models.KeyedVectors.load_word2vec_format(w2v_filename, binary=False)
        self.vocab_size = len(word2vec.wv.vocab)
        embedding_matrix = np.zeros((len(word2vec.wv.vocab), vector_dim))
        for i in range(self.vocab_size):
            embedding_vector = word2vec.wv[word2vec.wv.index2word[i]]
            if embedding_vector is not None:
                embedding_matrix[i] = embedding_vector
        self.embedding = tf.keras.layers.Embedding(self.vocab_size, self.vector_dim,
                                                   embeddings_initializer=tf.keras.initializers.Constant(
                                                       embedding_matrix), trainable=self.wv_trainable)
        self.lstm = layers.Bidirectional(layers.LSTM(self.hidden_size, dropout=0.5, return_sequences=True))
        self.fc1 = layers.TimeDistributed(layers.Dense(64, activation='relu'))
        self.fc2 = layers.Dense(1, activation='sigmoid')
        self.build(input_shape)

    def build(self, input_shape):
        inputs = tf.keras.Input(shape=input_shape, dtype=tf.float32)

        embedding_outs = self.embedding(inputs)

        lstm_outs = self.lstm(embedding_outs)
        fc1_outs = self.fc1(lstm_outs)
        fc1_outs = tf.reshape(fc1_outs, (-1, 64))
        outs = self.fc2(fc1_outs)
        self.built = True
        return outs

    def call(self, inputs):
        embedding_outs = self.embedding(inputs)
        lstm_outs = self.lstm(embedding_outs)
        fc1_outs = self.fc1(lstm_outs)
        fc1_outs = tf.reshape(fc1_outs, (-1, 64))
        outs = self.fc2(fc1_outs)
        return outs
import pandas as pd
import gensim
import numpy as np



class bilstm:
    def __init__(self,vector_dim):
        self.vector_dim=vector_dim
        word2vec=gensim.models.KeyedVectors.load_word2vec_format('wiki.zh.text.vector',binary=False)
        embedding_matrix=np.zeros((len(word2vec.wv.vocab),vector_dim))
        for i in range(len(word2vec.wv.vocab)):
            embedding_vector=word2vec.wv[word2vec.wv.index2word[i]]
            if embedding_vector is not None:
                embedding_matrix[i]=embedding_vector

        saved_embeddings=tf.constant(embedding_matrix)
        self.embedding=tf.Variable(initial_value=saved_embeddings,trainable=False)

from dao.xml_dao import XmlDao
from dao.new_file_dao import NewFileDao
from resources.file_paths import *
import numpy as np
import nltk
# from keras.models import Sequential, load_model
# from keras.layers import Dense
# from keras.layers import Dropout
# from keras.layers import LSTM
from gensim.models import Word2Vec
import pickle
import joblib

# FEATURE_SIZE = 128
FEATURE_SIZE = 64

class FeatureGenerator(object):
    def __init__(self):
        # dao = XmlDao()
        # self.labeled_articles, self.unlabeled_articles = dao.load_file()

        dao = NewFileDao()
        labeled_articles1, unlabeled_articles1 = dao.load_file(articles_file1)
        labeled_articles2, unlabeled_articles2 = dao.load_file(articles_file2)
        labeled_articles3, unlabeled_articles3 = dao.load_file(articles_file3)
        self.labeled_articles = labeled_articles1 + labeled_articles2 + labeled_articles3
        self.unlabeled_articles = unlabeled_articles1 + unlabeled_articles2 + unlabeled_articles3

        self.sentensor = nltk.data.load(nltk_pickle)
        self.w2v_model = self.w2v()

    def w2v(self):
        # 把所有句子都放到一个字符串里
        raw_texts = [''] * (len(self.labeled_articles) + len(self.unlabeled_articles))
        for i, article in enumerate(self.labeled_articles):
            raw_texts[i] = (article.background + article.methods + article.results)
        for j, article in enumerate(self.unlabeled_articles):
            raw_texts[len(self.labeled_articles) + j] = article.abstract
        raw_text = ' '.join(raw_texts)
        raw_text = raw_text.lower()
        sents = self.sentensor.tokenize(raw_text)
        corpus = []
        for sen in sents:
            corpus.append(nltk.word_tokenize(sen))
        w2v_model = Word2Vec(corpus, size=FEATURE_SIZE, window=5, min_count=3, workers=4)
        return w2v_model

    def compute_parameters(self):
        # 首先计算训练集的维度
        num_sents = []  # 计算每个摘要最多有多少个句子
        num_words = []  # 计算每个句子最多有多少个单词
        for article in self.labeled_articles:
            sentences = self.sentensor.tokenize(article.abstract)
            num_sents.append(len(sentences))
            for sen in sentences:
                sen_len = len(nltk.word_tokenize(sen))
                num_words.append(sen_len)
        for article in self.unlabeled_articles:
            sentences = self.sentensor.tokenize(article.abstract)
            num_sents.append(len(sentences))
            for sen in sentences:
                sen_len = len(nltk.word_tokenize(sen))
                num_words.append(sen_len)
        #############################################################
        # 看一下句子、词长度取多少合适
        from collections import Counter
        print(Counter(num_sents))
        print(Counter(num_words))
        ##############################################################
        # 限制max_sents、max_words
        max_sents = min(20, max(num_sents))
        max_words = min(50, max(num_words))
        print('max_sents: ', max_sents)
        print('max_words: ', max_words)

        return max_sents, max_words

    def build_x_y(self):
        vocab = self.w2v_model.wv.vocab
        max_sents, max_words = self.compute_parameters()

        # 构建训练集
        x = np.zeros((int(len(self.labeled_articles)), max_sents, max_words, FEATURE_SIZE), dtype=np.float)
        classify = np.zeros((int(len(self.labeled_articles)), max_sents, 3), dtype=np.float)
        y = np.zeros((int(len(self.labeled_articles)), 2), dtype=np.float)
        for i, article in enumerate(self.labeled_articles):
            sentence_b = self.sentensor.tokenize(article.background)
            sentence_m = self.sentensor.tokenize(article.methods)
            sentence_r = self.sentensor.tokenize(article.results)
            sentences = sentence_b + sentence_m + sentence_r

            # build y， y是摘要中每一句分类成background/methods/results的onehot结果
            for j in range(min(len(sentence_b), max_sents)):
                classify[i][j][0] = 1.0
            for j in range(min(len(sentence_b), max_sents), min(len(sentence_m), max_sents)):
                classify[i][j][1] = 1.0
            for j in range(min(len(sentence_m), max_sents), min(len(sentence_r), max_sents)):
                classify[i][j][2] = 1.0

            # build y_location, y_location是摘要中methods、results首句的位置
            y[i][0] = len(sentence_b)
            y[i][1] = len(sentence_b) + len(sentence_m)

            # build x
            for j, sen in enumerate(sentences):
                if j >= max_sents:
                    break
                words = nltk.word_tokenize(sen)
                w_stream = []
                # 先去掉不在vocab里的词
                for w in words:
                    if w in vocab:
                        w_stream.append(w)
                for k, w in enumerate(w_stream):
                    if k >= max_words:
                        break
                    x[i][j][k] = np.array(self.w2v_model[w])
        return x, y

    def build_x_unlabeled(self):
        # 从unlabeled_articles构建需要预测的集合
        vocab = self.w2v_model.wv.vocab
        max_sents, max_words = self.compute_parameters()

        x = np.zeros((int(len(self.unlabeled_articles)), max_sents, max_words, FEATURE_SIZE), dtype=np.float)
        for i, article in enumerate(self.unlabeled_articles):
            sentences = self.sentensor.tokenize(article.abstract)
            for j, sen in enumerate(sentences):
                if j >= max_sents:
                    break
                words = nltk.word_tokenize(sen)
                w_stream = []
                # 先去掉不在vocab里的词
                for w in words:
                    if w in vocab:
                        w_stream.append(w)
                for k, w in enumerate(w_stream):
                    if k >= max_words:
                        break
                    x[i][j][k] = np.array(self.w2v_model[w])
        return x


if __name__ == '__main__':
    feature_generator = FeatureGenerator()

    x, y = feature_generator.build_x_y()
    with open(x_y_file, 'wb') as f:
        joblib.dump(x, f)
        pickle.dump(y, f)

    x_unlabeled = feature_generator.build_x_unlabeled()
    with open(x_unlabeled_file, 'wb') as f:
        joblib.dump(x_unlabeled, f)
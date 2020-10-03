from keras.models import load_model
from resources.file_paths import *
from dao.new_file_dao import NewFileDao
import nltk
import joblib

class Article(object):
    def __init__(self):
        self.pmid = 0
        self.type = ''
        self.background = []
        self.methods = []
        self.results = []

def get_all_articles():
    """
    把labeled和unlabeled的都做完background、methods、results切分后放到一个list里
    """
    model = load_model(model_path)
    with open(x_unlabeled_file, 'rb') as f:
        x = joblib.load(f)
    x = x.reshape(x.shape[0], x.shape[1], x.shape[2] * x.shape[3])
    y = model.predict(x)
    sentensor = nltk.data.load(nltk_pickle)

    # 对无标签的摘要做分段，和有标签的组合成一个列表
    dao = NewFileDao()
    labeled_articles1, unlabeled_articles1 = dao.load_file(articles_file1)
    labeled_articles2, unlabeled_articles2 = dao.load_file(articles_file2)
    labeled_articles3, unlabeled_articles3 = dao.load_file(articles_file3)
    labeled_articles = labeled_articles1 + labeled_articles2 + labeled_articles3
    unlabeled_articles = unlabeled_articles1 + unlabeled_articles2 + unlabeled_articles3

    article_list = []
    for article in labeled_articles:
        art = Article()
        art.pmid = article.pmid
        art.type = 'labeled'
        art.background = sentensor.tokenize(article.background)
        art.methods = sentensor.tokenize(article.methods)
        art.results = sentensor.tokenize(article.results)
        article_list.append(art)
    for i, article in enumerate(unlabeled_articles):
        sentences = sentensor.tokenize(article.abstract)
        art = Article()
        art.pmid = article.pmid
        art.type = 'unlabeled'
        methods_start = int(round(y[i][0]))
        results_start = int(round(y[i][1]))
        art.background = sentences[:methods_start]
        art.methods = sentences[methods_start:results_start]
        art.results = sentences[results_start:]
        article_list.append(art)

    return article_list

if __name__ == '__main__':
    article_list = get_all_articles()
    with open(all_articles_file, 'wb') as f:
        joblib.dump(article_list, f)
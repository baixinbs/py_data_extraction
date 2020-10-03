import re

from dao.article_entity import LabeledArticle, UnlabeledArticle
from resources.file_paths import *

class NewFileDao(object):
    def __init__(self):
        pass

    def load_file(self, file_path):
        labeled_articles = []
        unlabeled_articles = []
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            content = content.replace('\n      ', '')
            articles = content.split('\n\n')
            for art in articles:
                art_items = re.split('\n', art)
                pmid = ''
                abstract = ''
                for x in art_items:
                    if x[:5] == 'PMID-':
                        pmid = x[5:]
                    if x[:5] == 'AB  -':
                        abstract = x[5:]
                has_methods = False
                has_results = False
                abstract = abstract.lower()
                if re.search('methods:', abstract):
                    has_methods = True
                    if re.search('results:', abstract.split('methods:', 1)[1]):
                        has_results = True
                if has_methods and has_results:
                    tmp_list = abstract.split('methods:', 1)
                    background = tmp_list[0]
                    methods_results = tmp_list[1]
                    tmp_list = methods_results.split('results:', 1)
                    methods = tmp_list[0]
                    results = tmp_list[1]
                    article = LabeledArticle(pmid, abstract, background, methods, results)
                    labeled_articles.append(article)
                else:
                    article = UnlabeledArticle(pmid, abstract)
                    unlabeled_articles.append(article)
        return labeled_articles, unlabeled_articles

if __name__ == '__main__':
    dao = NewFileDao()
    labeled_articles1, unlabeled_articles1 = dao.load_file(articles_file1)
    labeled_articles2, unlabeled_articles2 = dao.load_file(articles_file2)
    labeled_articles3, unlabeled_articles3 = dao.load_file(articles_file3)
    labeled_articles = labeled_articles1 + labeled_articles2 + labeled_articles3
    unlabeled_articles = unlabeled_articles1 + unlabeled_articles2 + unlabeled_articles3


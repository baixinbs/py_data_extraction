from resources.file_paths import *
import joblib
import nltk

from matchers.method_sentence_matcher import method_sentence_matcher
from matchers.result_sentence_matcher import result_sentence_matcher
from algorithm.get_all_articles import Article
from algorithm.get_all_articles import *

class ArticleChunk(object):
    def __init__(self):
        self.pmid = ''
        self.background = ''
        self.methods = []
        self.results = []

class EntityMatcher(object):
    def __init__(self):
        pass

    def load_articles(self):
        """
        载入全部文章
        """
        # with open(all_articles_file, 'rb') as f:
        #     articles = joblib.load(f)
        articles = get_all_articles()
        return articles

    def save_sample_articles(self):
        # 将部分article存储到pickle中，加快调试速度
        all_articles = self.load_articles()
        sample_articles = all_articles[:500]
        with open(sample_articles_file, 'wb') as f:
            joblib.dump(sample_articles, f)

        # 将部分unlabeled_articles存储到文本中，可以人来看
        cnt = 0
        with open(sample_unlabeled_text_file, 'w') as f:
            for art in all_articles:
                if art.type == 'unlabeled':
                    f.write(art.pmid + '\n')
                    f.write(art.type + '\n')
                    f.write('--background:' + '\n')
                    for i, sen in enumerate(art.background):
                        f.write(str(i) + ': ' + sen + '\n')
                    f.write('--methods:' + '\n')
                    for i, sen in enumerate(art.methods):
                        f.write(str(i) + ': ' + sen + '\n')
                    f.write('--results:' + '\n')
                    for i, sen in enumerate(art.results):
                        f.write(str(i) + ': ' + sen + '\n')
                    f.write('\n\n\n')
                    cnt += 1
                if cnt > 500:
                    break


    def load_sample_articles(self):
        """
        载入部分文章
        """
        with open(sample_articles_file, 'rb') as f:
            sample_articles = joblib.load(f)
        return sample_articles

    def generate_article_chunk_list(self):
        # articles = self.load_sample_articles()
        articles = self.load_articles()

        art_chunk_list = []
        for art in articles:
            art_chunk = ArticleChunk()
            art_chunk.pmid = art.pmid
            art_chunk.background = art.background

            methods = art.methods
            for sen in methods:
                m_sen = nltk.word_tokenize(sen)
                chunks = method_sentence_matcher(m_sen)
                art_chunk.methods.append(chunks)

            results = art.results
            for sen in results:
                m_sen = nltk.word_tokenize(sen)
                chunks = result_sentence_matcher(m_sen)
                art_chunk.results.append(chunks)

            art_chunk_list.append(art_chunk)
        return art_chunk_list

    def statics_article_chunk_list_methods(self, art_chunk_list, entity_name):
        """
        *cnt_art: 多少篇文章中出现了
        *cnt_total: 所有文章出现了多少次
        """
        cnt_art = 0
        cnt_total = 0
        for art in art_chunk_list:
            methods = art.methods
            has_found = False
            for sen in methods:
                for chunk in sen:
                    if chunk[1] == entity_name:
                        cnt_art += 1
                        has_found = True
                        break
                if has_found is True:
                    break
        for art in art_chunk_list:
            methods = art.methods
            for sen in methods:
                for chunk in sen:
                    if chunk[1] == entity_name:
                        cnt_total += 1
        return cnt_art, cnt_total


    def statics_article_chunk_list_results(self, art_chunk_list, entity_name):
        """
        *cnt_art: 多少篇文章中出现了
        *cnt_total: 所有文章出现了多少次
        """
        cnt_art = 0
        cnt_total = 0
        for art in art_chunk_list:
            results = art.results
            has_found = False
            for sen in results:
                for chunk in sen:
                    if chunk[1] == entity_name:
                        cnt_art += 1
                        has_found = True
                        break
                if has_found is True:
                    break
        for art in art_chunk_list:
            results = art.results
            for sen in results:
                for chunk in sen:
                    if chunk[1] == entity_name:
                        cnt_total += 1
        return cnt_art, cnt_total

    def statics_relations(self, art_chunk_list, common_entity_name):
        """统计有多少条关系"""
        common_2_value = {
            'BC': 'CO',
            'CL': 'PE',
            'HT': 'TV',
            'CM': 'CO',
            'AT': 'CT',
            'AI': 'CT',
            'AU': 'CT',
            'BI': 'PE',
            'TM': 'CT'
        }
        value_entity_name = common_2_value[common_entity_name]
        cnt_art = 0
        cnt_total = 0
        for art in art_chunk_list:
            results = art.results
            found_common = False
            found_value = False
            for sen in results:
                for chunk in sen:
                    if chunk[1] == common_entity_name:
                        found_common = True
                for chunk in sen:
                    if chunk[1] == value_entity_name:
                        found_value = True
                if found_value is True and found_common is True:
                    cnt_art += 1
                    break

        for art in art_chunk_list:
            results = art.results
            found_common = False
            found_value = False
            for sen in results:
                for chunk in sen:
                    if chunk[1] == common_entity_name:
                        found_common = True
                for chunk in sen:
                    if chunk[1] == value_entity_name:
                        found_value = True
                if found_value is True and found_common is True:
                    cnt_total += 1
        return cnt_art, cnt_total

if __name__ == '__main__':
    entity_matcher = EntityMatcher()
    articles = entity_matcher.load_articles()
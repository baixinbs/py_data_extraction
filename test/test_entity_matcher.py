import unittest
from algorithm.entity_matcher import EntityMatcher
from resources.file_paths import *
from algorithm.get_all_articles import Article
from resources.file_paths import *
import joblib
import nltk

class TestEntityMatcher(unittest.TestCase):

    def test_save_sample_articles(self):
        entity_matcher = EntityMatcher()
        entity_matcher.save_sample_articles()

    def test_load_articles(self):
        entity_matcher = EntityMatcher()
        articles = entity_matcher.load_articles()

    def test_load_sample_articles(self):
        entity_matcher = EntityMatcher()
        sample_articles = entity_matcher.load_sample_articles()

    def test_generate_article_chunk_list(self):
        entity_matcher = EntityMatcher()
        art_chunk_list = entity_matcher.generate_article_chunk_list()
        with open(chunk_result_file, 'w', encoding="utf-8") as f:
            for art in art_chunk_list:
                f.write(art.pmid + '\n')
                f.write('--background:\n')
                for sen in art.background:
                    f.write(sen)
                    f.write('\n')
                f.write('--methods:\n')
                for sen in art.methods:
                    for x in sen:
                        if x[1]:
                            f.write('<' + str(x) + '>')
                        else:
                            f.write(x[0])
                        f.write(' ')
                    f.write('\n')
                f.write('--results:\n')
                for sen in art.results:
                    for x in sen:
                        if x[1]:
                            f.write('<' + str(x) + '>')
                        else:
                            f.write(x[0])
                        f.write(' ')
                    f.write('\n')
                f.write('\n\n')


    ## 最后这三个test结果输出给丹宁
    def test_statics_article_chunk_list_methods(self):
        entity_matcher = EntityMatcher()
        art_chunk_list = entity_matcher.generate_article_chunk_list()
        entity_names = ['DN', 'SP', 'DW', 'DR', 'DO', 'DU']
        for x in entity_names:
            rst = entity_matcher.statics_article_chunk_list_methods(art_chunk_list, x)
            print(x, rst)


    def test_statics_article_chunk_list_results(self):
        entity_matcher = EntityMatcher()
        art_chunk_list = entity_matcher.generate_article_chunk_list()
        entity_names = ['DN', 'SP', 'DW', 'DO', 'DU', 'MP', 'BC', 'CL', 'HT', 'CM', 'AT', 'AI', 'AU', 'BI', 'TM', 'CO', 'TV', 'PE', 'CT']
        for x in entity_names:
            rst = entity_matcher.statics_article_chunk_list_results(art_chunk_list, x)
            print(x, rst)

    def test_statics_relation(self):
        entity_matcher = EntityMatcher()
        art_chunk_list = entity_matcher.generate_article_chunk_list()
        entity_names = ['BC', 'CL', 'HT', 'CM', 'AT', 'AI', 'AU', 'BI', 'TM']
        for x in entity_names:
            rst = entity_matcher.statics_relations(art_chunk_list, x)
            print(x, rst)

if __name__ == '__main__':
    unittest.main()
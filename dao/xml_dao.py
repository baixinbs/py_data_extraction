from xml.etree import ElementTree

class PubArticle1(object):
    def __init__(self, pmid, abstract):
        self.pmid = pmid
        self.abstract = abstract

class PubArticle2(object):
    def __init__(self, pmid, abstract, background, methods, results):
        self.pmid = pmid
        self.abstract = abstract
        self.background = background
        self.methods = methods
        self.results = results

class XmlDao(object):
    def __init__(self):
        self.file = 'E:\\data_extraction_forZhaoDanNing\\data\\extraction\\20000pubmed_result.xml'
        # self.file = 'E:\\data_extraction_forZhaoDanNing\\data\\extraction\\pubmed_result0522.xml'

    def load_file(self):
        ftree = ElementTree.parse(self.file)
        root = ftree.getroot()
        print(len(root))
        labeled_articles = []
        unlabeled_articles = []
        for pubmed_article in root:
            medline_citation = pubmed_article[0]
            pmid = medline_citation.find('PMID').text
            article = medline_citation.find('Article')
            try:
                abstract = article.find('Abstract')
            except:
                continue
            if not abstract:
                continue
            is_formalized_abstract = False
            has_methods = False
            has_results = False
            for x in abstract:
                if x.attrib.get('NlmCategory') == 'METHODS':
                    has_methods = True
                if x.attrib.get('NlmCategory') == 'RESULTS' and has_methods == True:
                    has_results = True
            if has_methods == True and has_results == True:
                is_formalized_abstract = True

            if is_formalized_abstract == False:
                abstract_text = abstract.find('AbstractText').text
                article = PubArticle1(pmid, abstract_text)
                if abstract_text:
                    unlabeled_articles.append(article)
            else:
                methods_index = 0
                results_index = 0
                for i, x in enumerate(abstract):
                    if x.attrib.get('NlmCategory') == 'METHODS':
                        methods_index = i
                    if x.attrib.get('NlmCategory') == 'RESULTS':
                        results_index = i
                background = ''
                methods = ''
                results = ''
                for i in range(methods_index):
                    if abstract[i].text:
                        background = background + abstract[i].text
                for i in range(methods_index, results_index):
                    if abstract[i].text:
                        methods = methods + abstract[i].text
                for i in range(results_index, len(abstract)):
                    if abstract[i].text:
                        results = results + abstract[i].text
                article = PubArticle2(pmid, background + ' '  + methods + ' ' + results, background, methods, results)
                labeled_articles.append(article)
        return labeled_articles, unlabeled_articles

if __name__ == '__main__':
    dao = XmlDao()
    labeled_articles, unlabeled_articles = dao.load_file()
    print(len(labeled_articles), len(unlabeled_articles))
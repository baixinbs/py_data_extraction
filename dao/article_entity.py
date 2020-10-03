class UnlabeledArticle(object):
    def __init__(self, pmid, abstract):
        self.pmid = pmid
        self.abstract = abstract

class LabeledArticle(object):
    def __init__(self, pmid, abstract, background, methods, results):
        self.pmid = pmid
        self.abstract = abstract
        self.background = background
        self.methods = methods
        self.results = results
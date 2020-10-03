from resources.file_paths import *
import re

def match_doesunit(sentence):
    keyword_set = {'mg/kg', 'mg/day', 'mg/m(2)', 'g',
                   'mg', 'mg',
                   'μg', 'ng', 'μmol'}
    rst = []
    for kw in keyword_set:
        for i, word in enumerate(sentence):
            if re.search('\d+-' + kw, word):
                rst.append((i, i+1, 'DU', word))
        for i in range(len(sentence) - 1):
            word = sentence[i]
            next_word = sentence[i+1]
            if re.search('\d+', word) and next_word == kw:
                rst.append((i, i+2, 'DU', word+' '+next_word))
    return rst


if __name__ == '__main__':
    sentence = ['this', 'doses', '2-mg', 'once', 'a', '1', 'mg/kg']
    print(match_doesunit(sentence))
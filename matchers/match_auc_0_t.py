from resources.file_paths import *
import re

def match_auc_0_t(sentence):
    keyword_set = {'auc 0-t', 'auc0-t', 'auc0-last', 'auc 0-last',
                   'auclast', 'auc last'}
    rst = []
    if len(sentence) <= 1:
        return rst
    for keyw in keyword_set:
        len_keyw = len(keyw.split(' '))
        for i in range(len(sentence) - len_keyw):
            words = []
            for j in range(len_keyw):
                words.append(sentence[i+j])
            words = ' '.join(words)
            if words == keyw:
                rst.append((i, i+len_keyw, 'AT', keyw))
    for w in sentence:
        if re.search('auc-\d+', w):
            rst.append((i, i+1, 'AT', w))
    return rst

if __name__ == '__main__':
    sentence = ['total', 'body', 'auc', '0-t', 'once', '95%cl', 'concentration', 'in', 'vivo', 'day']
    print(match_auc_0_t(sentence))
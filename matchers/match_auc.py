from resources.file_paths import *
import re

def match_auc(sentence):
    keyword_set = {'auc', 'auclast'}
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
                rst.append((i, i+len_keyw, 'AU', keyw))
    for w in sentence:
        if re.search(r'auc\S*-\S*', w):
            rst.append((i, i+1, 'AU', w))
    return rst

if __name__ == '__main__':
    sentence = ['total', 'body', 'auc', 'auc0-t', 'auc(0-inf)', '95%cl', 'concentration', 'in', 'vivo', 'day']
    print(match_auc(sentence))
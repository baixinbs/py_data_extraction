from resources.file_paths import *
import re

def match_percentage(sentence):
    rst = []
    for i, w in enumerate(sentence):
        if re.search(r'\S*%', w):
            rst.append((i, i + 1, 'PE', w))
    return rst

if __name__ == '__main__':
    sentence = ['total', 'body', 'auc', '0-t', 'once', '95%', 'concentration', 'in', 'vivo', 'day']
    print(match_percentage(sentence))
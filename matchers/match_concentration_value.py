from resources.file_paths import *

def match_concentration_value(sentence):
    keyword_set = {'microg/l', 'microg/ml', 'ng/ml', 'ug/ml', 'mg/ml', 'g/ml', 'micromol/l'}
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
                rst.append((i, i+len_keyw, 'CO', keyw))
    return rst

if __name__ == '__main__':
    sentence = ['total', 'body', 'auc', '0-t', 'once', '95%cl', 'concentration', 'in', 'vivo', 'day']
    print(match_concentration_value(sentence))
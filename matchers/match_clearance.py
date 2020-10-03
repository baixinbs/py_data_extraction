from resources.file_paths import *

def match_clearance(sentence):
    keyword_set = {'total body clearance','cl','clr',
                   '95%cl', '90cl'}
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
                rst.append((i, i+len_keyw, 'CL', keyw))
    return rst

if __name__ == '__main__':
    sentence = ['total', 'body', 'clearance', 'once', '95%cl', 'concentration', 'in', 'vivo', 'day']
    print(match_clearance(sentence))
from resources.file_paths import *

def match_c_max(sentence):
    keyword_set = {'cmax', 'c(max)'}
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
                rst.append((i, i+len_keyw, 'CM', keyw))
    return rst

if __name__ == '__main__':
    sentence = ['total', 'body', 'clearance', 'once', 'cmax', 'concentration', 'in', 'vivo', 'day']
    print(match_c_max(sentence))
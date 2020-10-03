from resources.file_paths import *

def match_half_time(sentence):
    keyword_set = {'half-life','t1/2','t(1/2)'}
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
                rst.append((i, i+len_keyw, 'HT', keyw))
    return rst

if __name__ == '__main__':
    sentence = ['total', 'half-life', 'clearance', 't1/2', '95%cl', 'concentration', 'in', 'vivo', 'day']
    print(match_half_time(sentence))
from resources.file_paths import *

def match_concentration(sentence):
    keyword_set = {'blood concentration','blood concentrations','plasma concentration','drug concentration in vivo',
                   'serum concentration'}
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
                rst.append((i, i+len_keyw, 'BC', keyw))
    return rst

if __name__ == '__main__':
    sentence = ['blood', 'concentration', 'doses', 'once', 'drug', 'concentration', 'in', 'vivo', 'day']
    print(match_concentration(sentence))
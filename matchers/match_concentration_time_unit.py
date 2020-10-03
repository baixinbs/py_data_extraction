from resources.file_paths import *

def match_concentration_time_unit(sentence):
    keyword_set = {'microg.l(-1).h', 'ng * hr/ml', 'ng x hr/ml', 'ng * h/ml',
                   'ng x h/ml', 'ng.h/ml', 'mg.h/l', 'mug min(-1) ml(-1)',
                   'microg * hour/ml', 'microg x hour/ml', 'ng min(-1) ml(-1)'}
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
                rst.append((i, i+len_keyw, 'CT', keyw))
    return rst

if __name__ == '__main__':
    sentence = ['total', 'mug', 'min(-1)', 'ml(-1)', 'auc', '0-t', 'once', '95%cl', 'concentration', 'in', 'vivo', 'day']
    print(match_concentration_time_unit(sentence))
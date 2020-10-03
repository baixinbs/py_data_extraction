from resources.file_paths import *

def match_time_value(sentence):
    keyword_set = {'minutes', 'minute', 'second', 'seconds', 'day', 'days', 'month', 'months', 'months'
                   'year', 'years', 'hour', 'hours', 'min', 'h', 'hr', 'hrs', 'd', 's'}
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
                rst.append((i, i+len_keyw, 'TV', keyw))
    return rst

if __name__ == '__main__':
    sentence = ['total', 'body', 'auc', '0-t', 'once', '95%cl', 'concentration', 'in', 'vivo', 'day']
    print(match_time_value(sentence))
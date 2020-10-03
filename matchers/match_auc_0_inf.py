from resources.file_paths import *

def match_auc_0_inf(sentence):
    keyword_set = {'auc 0-inf', 'auc0-inf', 'auc0-infinity', 'auc 0-infinity',
                   'auc0-∞', 'auc 0-∞'}
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
                rst.append((i, i+len_keyw, 'AI', keyw))
    return rst

if __name__ == '__main__':
    sentence = ['total', 'body', 'auc', '0-inf', 'once', '95%cl', 'concentration', 'in', 'vivo', 'day']
    print(match_auc_0_inf(sentence))
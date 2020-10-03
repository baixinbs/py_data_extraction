from resources.file_paths import *

def match_does(sentence):
    keyword_set = {'does', 'dosing', 'dosage', 'doses',
                   'single-does', 'multiple-does',
                   's.i.d', 'b.i.d', 't.i.d',
                   'daily', ('per','day'), ('a', 'day')}
    rst = []
    if len(sentence) <= 1:
        return rst
    for i in range(len(sentence) - 1):
        word = sentence[i]
        next_word = sentence[i + 1]
        if word in keyword_set:
            rst.append((i, i+1, 'DO', word))
        if (word, next_word) in keyword_set:
            rst.append((i, i+2, 'DO', word))
    return rst

if __name__ == '__main__':
    sentence = ['this', 'doses', 'once', 'a', 'day']
    print(match_does(sentence))
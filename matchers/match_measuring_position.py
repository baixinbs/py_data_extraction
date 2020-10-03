def match_measuring_position(m_sentence):
    key_words = {'plasma','hearts','heart','livers','liver','lungs','lung',
    'kidneys','kidney','muscles','muscle','brains','brain'}
    rst = []
    for i, word in enumerate(m_sentence):
        if word in key_words:
            rst.append((i, i+1, 'MP', word))
    return rst

if __name__ == '__main__':
    sentence = ['the', 'drug', 'plasma', 'is', 'livers', 'good', '!']
    rst = match_measuring_position(sentence)
    print(rst)
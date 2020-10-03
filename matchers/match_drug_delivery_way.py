from resources.file_paths import *

def match_drug_delivery_way(sentence, delivery_way_dict):
    rst = []
    if len(sentence) <= 1:
        return rst
    for i in range(len(sentence) - 1):
        word = sentence[i]
        next_word = sentence[i+1]
        if word in delivery_way_dict:
            rst.append((i, i+1, 'DW', delivery_way_dict.get(word)))
        if (word + ' ' + next_word) in delivery_way_dict:
            rst.append((i, i+2, 'DW', delivery_way_dict.get((word + ' ' + next_word))))
    return rst

def build_drug_delivery_way_dict():
    with open(drug_delivery_way_file, 'r') as f:
        delivery_way_list = f.readlines()
        delivery_way_list = [x.strip('\n') for x in delivery_way_list]
        delivery_way_dict = {}
        for x in delivery_way_list:
            same_ways = x.split('/')
            m_value = same_ways[-1]
            for w in same_ways:
                delivery_way_dict[w] = m_value
        return delivery_way_dict

if __name__ == '__main__':
    delivery_way_dict = build_drug_delivery_way_dict()
    print(delivery_way_dict)
    sentence = ['one', 'way', 'is', 'gavage', 'and', 'hypodermic', 'injection']
    rst = match_drug_delivery_way(sentence, delivery_way_dict)
    print(rst)
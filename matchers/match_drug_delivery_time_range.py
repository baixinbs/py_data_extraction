from resources.file_paths import *
import re

def match_drug_delivery_time_range(sentence, drug_delivery_time_range_list):
    """找到句子中为时间单位的词
    rst：（位置，时间单位词）
    """
    rst = []
    for i, word in enumerate(sentence):
        if word in drug_delivery_time_range_list and i > 0:
            if re.search('\d+', sentence[i-1]):
                rst.append((i-1, i + 1, 'DR', sentence[i-1] + ' ' + word))
        if word in drug_delivery_time_range_list and i < len(sentence) - 1:
            if re.search('\d+', sentence[i+1]):
                rst.append((i, i + 2, 'DR', word + ' ' + sentence[i+1]))
    return rst

def build_drug_delivery_time_range_list():
    with open(drug_delivery_time_range_file, 'r') as f:
        time_range_list = f.readlines()
        time_range_list = [x.strip('\n') for x in time_range_list]
        return set(time_range_list)

if __name__ == '__main__':
    drug_delivery_time_range_list = build_drug_delivery_time_range_list()
    print(drug_delivery_time_range_list)
    sentence = ['the', 'time', 'is', 'h', '1','10', 'hours', '2', 'minutes']
    rst = match_drug_delivery_time_range(sentence, drug_delivery_time_range_list)
    print(rst)
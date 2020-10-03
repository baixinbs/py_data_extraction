import pandas as pd
from resources.file_paths import *

def match_drug_name(m_sentence, dict_drug_name2id):
    """
    rst：（位置，长度，'DN', drug_name)
    """
    rst = []
    for i, word in enumerate(m_sentence):
        if word in dict_drug_name2id:
            rst.append((i, i+1, 'DN', word))
    return rst

def build_drug_name_dict():
    """
    生成两个字典，分别从drugname查询drugid，和从drugid查询drugname
    """
    drug_name = pd.read_csv(drug_names_file, encoding='utf-8')
    pd.set_option('display.max_columns', None)
    drug_name2id = {}
    for i, row in drug_name.iterrows():
        drug_name2id[row[2].lower()] = row[0].lower()

    return drug_name2id

if __name__ == '__main__':
    dict_drug_name2id = build_drug_name_dict()
    sentence = ['the', 'drug', 'gestrinone', 'is', 'really', 'good', '!']
    rst = match_drug_name(sentence, dict_drug_name2id)
    print(rst)
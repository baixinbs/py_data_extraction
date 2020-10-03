from resources.file_paths import *

def match_species(sentence, species_list):
    """
    rst：（位置，词）
    """
    rst = []
    for i, word in enumerate(sentence):
        if word in species_list:
            rst.append((i, i+1, 'SP', word))
    return rst

def build_species_list():
    with open(species_file, 'r') as f:
        species_list = f.readlines()
        species_list = [x.strip('\n') for x in species_list]
        return set(species_list)

if __name__ == '__main__':
    species_list = build_species_list()
    sentence = ['we', 'have', 'a', 'horse']
    rst = match_species(sentence, species_list)
    print(rst)
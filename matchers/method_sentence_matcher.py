from matchers.match_drug_name import *
from matchers.match_species import *
from matchers.match_drug_delivery_way import *
from matchers.match_drug_delivery_time_range import *
from matchers.match_does import *
from matchers.match_doesunit import *

dict_drug_name2id = build_drug_name_dict()
species_list = build_species_list()
delivery_way_dict = build_drug_delivery_way_dict()
drug_delivery_time_range_list = build_drug_delivery_time_range_list()

def method_sentence_matcher(sentence):
    entities = []
    entities = entities + match_drug_name(sentence, dict_drug_name2id)
    entities = entities + match_species(sentence, species_list)
    entities = entities + match_drug_delivery_way(sentence, delivery_way_dict)
    entities = entities + match_drug_delivery_time_range(sentence, drug_delivery_time_range_list)
    entities = entities + match_does(sentence)
    entities = entities + match_doesunit(sentence)
    entities.sort()
    chunks = []
    cur = 0
    for i in range(len(entities) - 1):
        start = entities[i][0]
        end = entities[i][1]
        for j in range(cur, start):
            chunks.append((sentence[j], ''))
        chunks.append((entities[i][3], entities[i][2]))
        cur = end
    for i in range(cur, len(sentence)):
        chunks.append((sentence[i], ''))
    return chunks
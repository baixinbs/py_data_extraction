from matchers.match_drug_name import *
from matchers.match_species import *
from matchers.match_drug_delivery_way import *
from matchers.match_does import *
from matchers.match_doesunit import *
from matchers.match_measuring_position import *
from matchers.match_concentration import *
from matchers.match_clearance import *
from matchers.match_half_time import *
from matchers.match_c_max import *
from matchers.match_auc_0_t import *
from matchers.match_auc_0_inf import *
from matchers.match_auc import *
from matchers.match_bioavailability import *
from matchers.match_t_max import *
from matchers.match_concentration_value import *
from matchers.match_time_value import *
from matchers.match_percentage import *
from matchers.match_concentration_time_unit import *


dict_drug_name2id = build_drug_name_dict()
species_list = build_species_list()
delivery_way_dict = build_drug_delivery_way_dict()

def result_sentence_matcher(sentence):
    entities = []
    entities = entities + match_drug_name(sentence, dict_drug_name2id)
    entities = entities + match_species(sentence, species_list)
    entities = entities + match_drug_delivery_way(sentence, delivery_way_dict)
    entities = entities + match_does(sentence)
    entities = entities + match_doesunit(sentence)
    entities = entities + match_measuring_position(sentence)
    entities = entities + match_concentration(sentence)
    entities = entities + match_clearance(sentence)
    entities = entities + match_half_time(sentence)
    entities = entities + match_c_max(sentence)
    entities = entities + match_auc_0_t(sentence)
    entities = entities + match_auc_0_inf(sentence)
    entities = entities + match_auc(sentence)
    entities = entities + match_bioavailability(sentence)
    entities = entities + match_t_max(sentence)
    entities = entities + match_concentration_value(sentence)
    entities = entities + match_time_value(sentence)
    entities = entities + match_percentage(sentence)
    entities = entities + match_concentration_time_unit(sentence)
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
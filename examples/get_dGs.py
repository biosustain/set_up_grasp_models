import os

from set_up_grasp_models.set_up_models.set_up_thermo_rxns import get_dGs
from set_up_grasp_models.io.plaintext import import_model_from_plaintext


file_rxns = os.path.join('models', 'model_with_PPP_plaintext.txt')
file_bigg_kegg_ids = os.path.join('..', 'data', 'map_bigg_to_kegg_ids.csv')

model = import_model_from_plaintext(file_rxns)
rxn_list = model.to_string().split('\n')

rxn_dG_dict = get_dGs(rxn_list, file_bigg_kegg_ids, pH=7.0, ionic_strength=0.1, digits=2)

print(rxn_dG_dict)
import os

from set_up_grasp_models.set_up_models.set_up_thermo_rxns import get_dGs


file_rxns = os.path.join('models', 'putida_with_PPP_plaintext.txt')
file_bigg_kegg_ids = os.path.join('..', 'data', 'map_bigg_to_kegg_ids.csv')

rxn_dG_dict = get_dGs(file_rxns, file_bigg_kegg_ids, pH=7.0, ionic_strength=0.1, digits=2)

print(rxn_dG_dict)
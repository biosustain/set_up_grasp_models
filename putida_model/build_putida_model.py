from src.set_up_grasp_models.set_up_model import set_up_model


file_in_stoic = '/home/mrama/Dropbox/Postdoc/Putida/models/putida_with_PPP_plaintext.txt'
general_file = '../base_files/GRASP_general.xlsx'
model_name = 'putida_v1'
file_out = '/home/mrama/Dropbox/Postdoc/Putida/models/putida_v1.xlsx'

set_up_model(file_in_stoic, general_file, model_name, file_out)
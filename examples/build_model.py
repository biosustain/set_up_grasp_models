from set_up_grasp_models.set_up_models.set_up_model import set_up_model
from set_up_grasp_models.check_models.mass_balance_checks import check_flux_balance
import pandas as pd
import os


def generate_base_model():

    file_in_stoic = os.path.join('build_model', 'model_with_PPP_plaintext.txt')
    general_file = os.path.join('..', 'base_files', 'GRASP_general.xlsx')
    model_name = 'model_v1'
    file_out = os.path.join('build_model', model_name + '.xlsx')

    set_up_model(model_name, file_in_stoic, general_file, file_out)


def check_fluxes():

    file_in = os.path.join('build_model', 'model_v1_manual3.xlsx')
    data_dict = pd.read_excel(file_in, sheet_name=None)
    check_flux_balance(data_dict)


def generate_model_from_base():

    file_in_stoic = os.path.join('build_model', 'model_with_PPP_plaintext.txt')
    base_excel_file = os.path.join('build_model', 'model_v1_manual2_EX.xlsx')
    model_name = 'model_v2'
    file_in_mets_conc = os.path.join('build_model', 'met_concs.xlsx')

    file_out = os.path.join('build_model', model_name + '.xlsx')

    set_up_model(model_name, file_in_stoic, base_excel_file, file_out, use_equilibrator=True,
                 file_in_mets_conc=file_in_mets_conc)


#generate_base_model()
#check_fluxes()
generate_model_from_base()

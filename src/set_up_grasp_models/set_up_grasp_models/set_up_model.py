import numpy as np
import pandas as pd

from ..io.plaintext import import_model_from_plaintext


def get_stoic(file_in):
    """
    From a text file with the reactions in the model, set up a dataframe with the transposed stoichiometry matrix.

    Args:
        file_in: file path to

    Returns:
        tuple:  pandas dataframe with tranposed stoichiometry matrix, list with metabolites order,
                list with reactions order.
    """

    model = import_model_from_plaintext(file_in)
    mets_order = list(model.metabolites.keys())
    rxns_order = list(model.reactions.keys())

    stoic_df = pd.DataFrame(model.stoichiometric_matrix(), columns=rxns_order, index=mets_order)
    stoic_df = stoic_df.transpose()
    print(stoic_df)

    return stoic_df, mets_order, rxns_order


def update_stoic(stoic_df, ex_rxns, ex_mets, non_ex_mets_order):
    """
    Updates the stoichiometry matrix dataframe by removing the exchange reactions that are not used and the
    external metabolites no longer involved in the model.

    Args:
        stoic_df: pandas dataframe with stoichiometry matrix
        ex_rxns: list with exchange reactions active in the model
        ex_mets: list with exchange metabolites active in the model
        non_ex_mets_order: list with the order of non-external metabolites

    Returns:
        tuple: pandas dataframe with tranposed stoichiometry matrix, list with metabolites order,
                list with reactions order, list with exchange reactions to remove,
                list with external metabolites to remove.
    """

    all_ex_rxns = set(stoic_df.filter(regex='EX_', axis=0).index.values)
    ex_rxns_to_remove = all_ex_rxns.difference(ex_rxns)

    stoic_df = stoic_df.drop(ex_rxns_to_remove)
    ex_mets_to_remove = stoic_df.loc[:, (stoic_df == 0).all(axis=0)].columns.values

    stoic_df = stoic_df.loc[:, (stoic_df != 0).any(axis=0)]

    if non_ex_mets_order:
        non_ex_mets_order.extend(ex_mets)
        stoic_df = stoic_df.reindex(columns=non_ex_mets_order)
    stoic_df.index.name = 'rxn ID'
    print(stoic_df)
    mets_order = stoic_df.columns.values
    rxns_order = stoic_df.index.values

    return stoic_df, mets_order, rxns_order, ex_rxns_to_remove, ex_mets_to_remove


def set_up_model(file_in_stoic, base_excel_file, model_name, file_out, file_in_met_ranges=None, file_in_prot_ranges=None,
                 file_in_ex_fluxes=None, file_in_kinetics=None):

    writer = pd.ExcelWriter(file_out, engine='xlsxwriter')

    # set up general
    general_df = pd.read_excel(base_excel_file, index_col=0, header=0, sheet_name='general')
    print(general_df)
    general_df.iloc[0, 0] = model_name
    print(general_df)
    general_df.to_excel(writer, sheet_name='general')


    # set up stoic
    stoic_df, mets_order, rxns_order = get_stoic(file_in_stoic)
    stoic_df.to_excel(writer, sheet_name='stoic')


    # write mets
    columns = ['Metabolite name', 'balanced?', 'active?', 'fixed?']
    mets_df = pd.DataFrame(index=mets_order, columns=columns, data=np.zeros([len(mets_order), len(columns)]))
    mets_df.index.name = 'ID'
    mets_df.to_excel(writer, sheet_name='mets')

    # set up rxns
    columns = ['reaction name', 'transportRxn?', 'modelled?']
    rxns_df = pd.DataFrame(index=rxns_order, columns=columns, data=np.zeros([len(rxns_order), len(columns)]))
    rxns_df.index.name = 'ID'
    rxns_df.to_excel(writer, sheet_name='rxns')

    # set up splitRatios
    split_ratios_df = pd.DataFrame(index=rxns_order)
    split_ratios_df.index.name = 'ID'
    split_ratios_df.to_excel(writer, sheet_name='splitRatios')

    # set up poolConst
    pool_const_df = pd.DataFrame(index=mets_order)
    pool_const_df.index.name = 'met'
    pool_const_df.to_excel(writer, sheet_name='poolConst')

    # set up thermo_ineq_constraints
    thermo_ineq_constraints_df = pd.DataFrame(index=mets_order)
    thermo_ineq_constraints_df.index.name = 'met'
    thermo_ineq_constraints_df.to_excel(writer, sheet_name='thermo_ineq_constraints')

    # set up thermoRxns
    columns = ['∆Gr\'_min (kJ/mol)', '∆Gr\'_max (kJ/mol)']
    thermo_rxns_df = pd.DataFrame(index=rxns_order, columns=columns, data=np.zeros([len(rxns_order), len(columns)]))
    thermo_rxns_df.index.name = 'rxn'
    thermo_rxns_df.to_excel(writer, sheet_name='thermoRxns')

    # set up thermoMets
    columns = ['min (M)', 'max (M)']
    thermo_mets_df = pd.DataFrame(index=mets_order, columns=columns, data=np.zeros([len(mets_order), len(columns)]))
    thermo_mets_df.index.name = 'met'
    thermo_mets_df.to_excel(writer, sheet_name='thermoMets')

    # set up measRates
    columns = ['MBo10_mean', 'MBo10_std', 'MBo10_mean2', 'MBo10_std2']
    meas_rates_df = pd.DataFrame(index=rxns_order, columns=columns, data=np.zeros([len(rxns_order), len(columns)]))
    meas_rates_df.index.name = 'Fluxes (umol/gdcw/h)'
    meas_rates_df.to_excel(writer, sheet_name='measRates')

    # set up protData
    columns = ['MBo10_LB2', 'MBo10_meas2', 'MBo10_UB2']
    prot_data_df = pd.DataFrame(index=rxns_order, columns=columns, data=np.zeros([len(rxns_order), len(columns)]))
    prot_data_df.index.name = 'enzyme/rxn'
    prot_data_df.to_excel(writer, sheet_name='protData')

    # set up metsData
    columns = ['MBo10_LB2', 'MBo10_meas2', 'MBo10_UB2']
    mets_data_df = pd.DataFrame(index=mets_order, columns=columns, data=np.zeros([len(mets_order), len(columns)]))
    mets_data_df.index.name = 'met'
    mets_data_df.to_excel(writer, sheet_name='metsData')

    # set up kinetics1
    columns = ['kinetic mechanism', 'order', 'promiscuous', 'inhibitors', 'activators',
               'negative effector', 'positive effector', 'allosteric', 'subunits', 'comments']
    kinetics_df = pd.DataFrame(index=rxns_order, columns=columns, data=np.zeros([len(rxns_order), len(columns)]))
    kinetics_df.index.name = 'reaction ID'
    kinetics_df.to_excel(writer, sheet_name='kinetics1')

    writer.save()
    return 0

""""

def prepare_set_up_models(strain, time_point, replicate):

    file_in_base_model ='/home/mrama/Dropbox/Postdoc/HMP/HMP_base_python2.xlsx'
    file_in_stoich = '/home/mrama/Dropbox/Postdoc/HMP/HMP_stoich.txt'

    model_id = ''.join([strain, '_r', str(replicate), '_t', str(time_point)])
    file_in_met_ranges = ''.join(['/home/mrama/Dropbox/Postdoc/HMP/metabolomics/met_ranges_', model_id, '.csv'])
    file_in_prot_ranges = '/home/mrama/Dropbox/Postdoc/HMP/proteomics/technical_reproducibility/EXP_17_DL5596_Technical_reproducibility_normalized_results_std_all.csv'
    file_in_ex_fluxes = ''.join(['/home/mrama/Dropbox/Postdoc/HMP/metabolomics/ex_fluxes_', strain, '.csv'])
    file_out = ''.join(['/home/mrama/GRASP_test/GRASP/input_HMP_quadratic_splines/', model_id, '.xlsx'])

    # get constant dataframes

    general_df = pd.read_excel(file_in_base_model, sheet_name='general', index_col=0)
    general_df.iloc[0, 0] = model_id + '_promiscuous'

    map_met_abbreviation = {'accoa': 'accoa_c', 'coa': 'coa_c', 'tryptophan': 'trp_c', '5-htp': 'fivehtp_c', 'serotonin': 'srtn_c',
                                'acetylserotonin': 'nactsertn_c', 'melatonin': 'meltn_c', 'tryptamine': 'tryptm_c',
                                'acetyltryptamine': 'nactryptm_c', 'melatonin_e': 'meltn_e', 'serotonin_e': 'srtn_e',
                                'acetylserotonin_e': 'nactsertn_e', 'tryptamine_e': 'tryptm_e',
                                'acetyltryptamine_e': 'nactryptm_e', 'tryptophan_e': 'trp_e', '5-htp_e': 'fivehtp_e',
                                'sam': 'sam_c', 'sah': 'sah_c'}

    map_prot_abbreviation = {'hsTpH': 'TPH', 'ckDDC': 'DDC', 'sgAANAT': 'AANAT', 'hsASMT': 'ASMT'}

    non_ex_mets_order = ['accoa_c', 'sam_c', 'pterin1_c',  'trp_v', 'fivehtp_c', 'trp_c',  'srtn_c', 'nactsertn_c', 'meltn_c',
                         'tryptm_c', 'nactryptm_c', 'coa_c', 'sah_c', 'pterin2_c']
    #non_ex_mets_order = None

    set_up_model(file_in_base_model, file_in_stoich, file_in_met_ranges, file_in_prot_ranges, file_in_ex_fluxes, file_out,
                 general_df, map_met_abbreviation, map_prot_abbreviation, non_ex_mets_order, time_point, replicate)


def generate_models():

    strain_list = ['HMP1489', 'HMP2360']
    replicate_list = [0, 1]
    time_poins_list = range(4)

    for strain in strain_list:
        for replicate in replicate_list:
            for time_point in time_poins_list:
                prepare_set_up_models(strain, time_point, replicate)


if __name__ == '__main__':
    generate_models()
    
"""
import pandas as pd

from src.io.plaintext import read_model_from_file
from src.set_up_grasp_models.set_up_mets import set_up_mets, set_up_mets_data, set_up_thermo_mets
from src.set_up_grasp_models.set_up_proteomics import set_up_proteomics
from src.set_up_grasp_models.set_up_rates import set_up_ex_rates, set_up_rxns, set_up_kinetics, set_up_thermo_rxns


def get_stoic(file_in):
    """
    From a text file with the reactions in the model, set up a dataframe with the transposed stoichiometry matrix.

    :param file_in: file path to
    :return:
        stoich_df: pandas dataframe with tranposed stoichiometry matrix.
        mets_order: list with metabolites order.
        rxns_order: list with reactions order.
    """

    model = read_model_from_file(file_in)
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

    :param stoic_df: pandas dataframe with stoichiometry matrix
    :param ex_rxns:  list with exchange reactions active in the model
    :param ex_mets:  list with exchange metabolites active in the model
    :param non_ex_mets_order:  list with the order of non-external metabolites
    :return:
        stoich_df: pandas dataframe with tranposed stoichiometry matrix.
        mets_order: list with metabolites order.
        rxns_order: list with reactions order.
        ex_rxns_to_remove: list with exchange reactions to remove.
        ex_mets_to_remove:  list with external metabolites to remove.
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


def set_up_model(file_in_base_model, file_in_stoic, file_in_met_ranges, file_in_prot_ranges, file_in_ex_fluxes, file_out,
                 general_df, map_met_abbreviation, map_prot_abbreviation, non_ex_mets_order, time_point, replicate):
    """
    Given the model stoichiometry and omics data, creates an excel file to be the for GRASP.

    :param file_in_base_model: an excel file with the sheets: general, mets, rxns, thermoRxns, kinetics1.
    :param file_in_stoic: a text file with all reactions in the model.
    :param file_in_met_ranges: an excel file with the metabolite ranges - both for metsData and thermoMets
    :param file_in_prot_ranges: an excel file with the protein ranges for protData
    :param file_in_ex_fluxes: an excel file with all exchange fluxes for measRates
    :param file_out: the output excel file (with path)
    :param general_df: the dataframe for the general sheet
    :param map_met_abbreviation: a dictionary with the metabolites full name used in the original omics data and the corresponding abbreviation for the model
    :param map_prot_abbreviation: a dictionary with the protein name used in the original omics data and
    :param non_ex_mets_order: list with metabolites order excluding the external ones
    :param time_point: time point for the model
    :param replicate: replicate for the model
    :return: None
    """

    # get base stoichiometry
    stoic_df, mets_order, rxns_order = get_stoic(file_in_stoic)

    # get measRates df
    ex_rates_df, ex_rxns, ex_mets = set_up_ex_rates(rxns_order, file_in_ex_fluxes, map_met_abbreviation, time_point,
                                                    replicate, only_EX=True)

    writer = pd.ExcelWriter(file_out, engine='xlsxwriter')

    # set up general
    general_df.to_excel(writer, sheet_name='general')

    # set up stoic
    stoic_df, mets_order, rxns_order, ex_rxns_to_remove, ex_mets_to_remove = update_stoic(stoic_df, ex_rxns, ex_mets,
                                                                                          non_ex_mets_order)
    stoic_df.to_excel(writer, sheet_name='stoic')

    # set up mets
    mets_df = set_up_mets(file_in_base_model, mets_order, ex_mets_to_remove)
    mets_df.to_excel(writer, sheet_name='mets')

    # set up rxns
    rxns_df = set_up_rxns(file_in_base_model, rxns_order, ex_rxns_to_remove)
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
    thermo_rxns_df = set_up_thermo_rxns(file_in_base_model, rxns_order, ex_rxns)
    thermo_rxns_df.to_excel(writer, sheet_name='thermoRxns')

    # set up thermoMets
    thermo_mets_df = set_up_thermo_mets(mets_order, file_in_met_ranges, map_met_abbreviation, met_lb=10**-12, met_ub=10**-8)
    thermo_mets_df.to_excel(writer, sheet_name='thermoMets')

    # set up measRates
    ex_rates_df.to_excel(writer, sheet_name='measRates')

    # set up protData
    prot_data_df = set_up_proteomics(rxns_order, ex_rxns, file_in_prot_ranges, map_prot_abbreviation, time_point, replicate, prot_lb = 0.99, prot_ub=1.01)
    prot_data_df.to_excel(writer, sheet_name='protData')

    # set up metsData
    mets_data_df = set_up_mets_data(mets_order, file_in_met_ranges, map_met_abbreviation, met_lb=0.99, met_ub=1.01)
    mets_data_df.to_excel(writer, sheet_name='metsData')

    # set up kinetics1
    kinetics_df = set_up_kinetics(file_in_base_model, rxns_order, ex_rxns)
    kinetics_df.to_excel(writer, sheet_name='kinetics1')

    writer.save()
    return 0


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
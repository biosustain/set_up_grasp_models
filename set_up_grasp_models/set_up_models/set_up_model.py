import numpy as np
import pandas as pd

from ..io.plaintext import import_model_from_plaintext


def get_stoic(file_in: str) -> tuple:
    """
    From a text file with the reactions in the model, set up a dataframe with the transposed stoichiometric matrix.

    Args:
        file_in (str): path to plain text file with the model reactions.

    Returns:
        stoic_df (pd.Dataframe): pandas dataframe with tranposed stoichiometric matrix.
        mets_order (list): list with metabolites order.
        rxns_order (list): list with reactions order.
    """

    model = import_model_from_plaintext(file_in)
    mets_order = list(model.metabolites.keys())
    rxns_order = list(model.reactions.keys())

    stoic_df = pd.DataFrame(model.stoichiometric_matrix(), columns=rxns_order, index=mets_order)
    stoic_df = stoic_df.transpose()
    stoic_df.index.name = 'rxn ID'

    return stoic_df, mets_order, rxns_order


def update_stoic(stoic_df: pd.DataFrame, ex_rxns: list, ex_mets: list, non_ex_mets_order: list) -> tuple:
    """
    Updates the stoichiometry matrix dataframe by removing the exchange reactions that are not used and the
    external metabolites no longer involved in the model.

    Args:
        stoic_df: pandas dataframe with stoichiometry matrix
        ex_rxns: list with exchange reactions active in the model
        ex_mets: list with exchange metabolites active in the model
        non_ex_mets_order: list with the order of non-external metabolites

    Returns:
        stoic_df (pd.Dataframe): pandas dataframe with tranposed stoichiometric matrix
        mets_order (list): list with metabolites order.
        rxns_order (list): list with reactions order.
        ex_rxns_to_remove (list): list with exchange reactions to remove.
        ex_mets_to_remove (list): list with external metabolites to remove
    """

    all_ex_rxns = set(stoic_df.filter(regex='EX_', axis=0).index.values)
    ex_rxns_to_remove = all_ex_rxns.difference(ex_rxns)

    stoic_df = stoic_df.drop(ex_rxns_to_remove)
    ex_mets_to_remove = stoic_df.loc[:, (stoic_df == 0).all(axis=0)].columns.values

    stoic_df = stoic_df.loc[:, (stoic_df != 0).any(axis=0)]

    if non_ex_mets_order:
        non_ex_mets_order.extend(ex_mets)
        stoic_df = stoic_df.reindex(columns=non_ex_mets_order)

    mets_order = stoic_df.columns.values
    rxns_order = stoic_df.index.values

    return stoic_df, mets_order, rxns_order, ex_rxns_to_remove, ex_mets_to_remove


def set_up_model(model_name: str, file_in_stoic: str, base_excel_file: str, file_out: str,
                 file_in_met_ranges=None, file_in_prot_ranges=None, file_in_ex_fluxes=None, file_in_kinetics=None):
    """
    Sets up the excel input model file template. A base excel file must be given. This file must contain at least
    the general sheet, for that one can use the file 'GRASP_general.xlsx' in base_files. In this case an excel
    file with all fields to be filled is generated.

    If a base excel file with some of the sheets already filled or partially filled is available then  whatever fields
    are already filled will be copied to the output model file.

    Args:
        model_name (str): name for the model.
        file_in_stoic (str): path to plain text file with reactions in the model.
        base_excel_file (str): path to the excel file to be used as a base.
        file_out (str): path to the output file.
        file_in_met_ranges:
        file_in_prot_ranges:
        file_in_ex_fluxes:
        file_in_kinetics:

    Returns:
        None
    """

    writer = pd.ExcelWriter(file_out, engine='xlsxwriter')

    base_df = pd.read_excel(base_excel_file, index_col=0, header=0, sheet_name=None)

    # set up general
    try:
        general_df = base_df['general']
    except KeyError:
        raise KeyError(f'The base excel file {base_excel_file} must contain a sheet named \'general\'')
    general_df.iloc[0, 0] = model_name
    general_df.to_excel(writer, sheet_name='general')

    # set up stoic
    stoic_df, mets_order, rxns_order = get_stoic(file_in_stoic)
    stoic_df.to_excel(writer, sheet_name='stoic')

    # set up mets
    columns = ['Metabolite name', 'balanced?', 'active?', 'fixed?']
    mets_df = pd.DataFrame(index=mets_order, columns=columns, data=np.zeros([len(mets_order), len(columns)]))
    mets_df.index.name = 'ID'
    if 'mets' in base_df.keys():
        index_intersection = set(base_df['mets'].index.values).intersection(mets_df.index.values)
        mets_df.loc[index_intersection, :] = base_df['mets'].loc[index_intersection, :]
    mets_df.to_excel(writer, sheet_name='mets')

    # set up rxns
    columns = ['reaction name', 'transportRxn?', 'modelled?', 'isoenzymes']
    rxns_df = pd.DataFrame(index=rxns_order, columns=columns, data=np.zeros([len(rxns_order), len(columns)]))
    rxns_df.index.name = 'ID'
    if 'rxns' in base_df.keys():
        index_intersection = set(base_df['rxns'].index.values).intersection(rxns_df.index.values)
        rxns_df.loc[index_intersection, :] = base_df['rxns'].loc[index_intersection, :]
    rxns_df.to_excel(writer, sheet_name='rxns')

    # set up splitRatios
    split_ratios_df = pd.DataFrame(index=rxns_order)
    split_ratios_df.index.name = 'ID'
    if 'splitRatios' in base_df.keys():
        index_intersection = set(base_df['splitRatios'].index.values).intersection(split_ratios_df.index.values)
        split_ratios_df.loc[index_intersection, :] = base_df['splitRatios'].loc[index_intersection, :]
    split_ratios_df.to_excel(writer, sheet_name='splitRatios')

    # set up poolConst
    pool_const_df = pd.DataFrame(index=mets_order)
    pool_const_df.index.name = 'met'
    if 'poolConst' in base_df.keys():
        index_intersection = set(base_df['poolConst'].index.values).intersection(pool_const_df.index.values)
        pool_const_df.loc[index_intersection, :] = base_df['poolConst'].loc[index_intersection, :]
    pool_const_df.to_excel(writer, sheet_name='poolConst')

    # set up thermo_ineq_constraints
    thermo_ineq_constraints_df = pd.DataFrame(index=mets_order)
    thermo_ineq_constraints_df.index.name = 'met'
    if 'thermo_ineq_constraints' in base_df.keys():
        index_intersection = set(base_df['thermo_ineq_constraints'].index.values).intersection(
            thermo_ineq_constraints_df.index.values)
        thermo_ineq_constraints_df.loc[index_intersection, :] = base_df['thermo_ineq_constraints'].loc[index_intersection, :]
    thermo_ineq_constraints_df.to_excel(writer, sheet_name='thermo_ineq_constraints')

    # set up thermoRxns
    columns = ['∆Gr\'_min (kJ/mol)', '∆Gr\'_max (kJ/mol)']
    thermo_rxns_df = pd.DataFrame(index=rxns_order, columns=columns, data=np.zeros([len(rxns_order), len(columns)]))
    thermo_rxns_df.index.name = 'rxn'
    if 'thermoRxns' in base_df.keys():
        index_intersection = set(base_df['thermoRxns'].index.values).intersection(thermo_rxns_df.index.values)
        thermo_rxns_df.loc[index_intersection, :] = base_df['thermoRxns'].loc[index_intersection, :]
    thermo_rxns_df.to_excel(writer, sheet_name='thermoRxns')

    # set up thermoMets
    columns = ['min (M)', 'max (M)']
    thermo_mets_df = pd.DataFrame(index=mets_order, columns=columns, data=np.zeros([len(mets_order), len(columns)]))
    thermo_mets_df.index.name = 'met'
    if 'thermoMets' in base_df.keys():
        index_intersection = set(base_df['thermoMets'].index.values).intersection(thermo_mets_df.index.values)
        thermo_mets_df.loc[index_intersection, :] = base_df['thermoMets'].loc[index_intersection, :]
    thermo_mets_df.to_excel(writer, sheet_name='thermoMets')

    # set up measRates
    columns = ['MBo10_mean', 'MBo10_std', 'MBo10_mean2', 'MBo10_std2']
    meas_rates_df = pd.DataFrame(index=rxns_order, columns=columns, data=np.zeros([len(rxns_order), len(columns)]))
    meas_rates_df.index.name = 'Fluxes (umol/gdcw/h)'
    if 'measRates' in base_df.keys():
        index_intersection = set(base_df['measRates'].index.values).intersection(meas_rates_df.index.values)
        meas_rates_df.loc[index_intersection, :] = base_df['measRates'].loc[index_intersection, :]
    meas_rates_df.to_excel(writer, sheet_name='measRates')

    # set up protData
    columns = ['MBo10_LB2', 'MBo10_meas2', 'MBo10_UB2']
    prot_data_df = pd.DataFrame(index=rxns_order, columns=columns, data=np.tile(np.array([0.99, 1.00, 1.01]),
                                                                                (len(rxns_order), 1)))
    prot_data_df.index.name = 'enzyme/rxn'
    if 'protData' in base_df.keys():
        index_intersection = set(base_df['protData'].index.values).intersection(prot_data_df.index.values)
        prot_data_df.loc[index_intersection, :] = base_df['protData'].loc[index_intersection, :]
    prot_data_df.to_excel(writer, sheet_name='protData')

    # set up metsData
    columns = ['MBo10_LB2', 'MBo10_meas2', 'MBo10_UB2']
    mets_data_df = pd.DataFrame(index=mets_order, columns=columns, data=np.tile(np.array([0.99, 1.00, 1.01]),
                                                                                (len(mets_order), 1)))
    mets_data_df.index.name = 'met'
    if 'metsData' in base_df.keys():
        index_intersection = set(base_df['metsData'].index.values).intersection(mets_data_df.index.values)
        mets_data_df.loc[index_intersection, :] = base_df['metsData'].loc[index_intersection, :]
    mets_data_df.to_excel(writer, sheet_name='metsData')

    # set up kinetics1
    columns = ['kinetic mechanism', 'substrate order', 'product order', 'promiscuous', 'inhibitors',
               'activators', 'negative effector', 'positive effector', 'allosteric', 'subunits',
               'mechanism_ref_type', 'mechanism_ref', 'inhibitors_ref_type', 'inhibitors_ref',
               'activators_ref_type', 'activators_ref', 'negative_effectors_ref_type', 'negative_effectors_ref',
               'positive_effectors_ref_type', 'positive_effectors_ref', 'subunits_ref_type', 'subunits_ref',
               'comments']
    kinetics_df = pd.DataFrame(index=rxns_order, columns=columns, data=np.zeros([len(rxns_order), len(columns)]))
    kinetics_df.index.name = 'reaction ID'
    if 'kinetics1' in base_df.keys():
        index_intersection = set(base_df['kinetics1'].index.values).intersection(kinetics_df.index.values)
        kinetics_df.loc[index_intersection, :] = base_df['kinetics1'].loc[index_intersection, :]
    kinetics_df.to_excel(writer, sheet_name='kinetics1')

    writer.save()

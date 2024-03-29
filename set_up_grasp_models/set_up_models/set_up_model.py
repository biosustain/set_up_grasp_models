import numpy as np
import pandas as pd

from set_up_grasp_models.io.plaintext import import_model_from_plaintext
from set_up_grasp_models.set_up_models.set_up_mets import _get_mets_conc, _set_up_thermo_mets, _set_up_mets_data
from set_up_grasp_models.set_up_models.set_up_thermo_rxns import _set_up_model_thermo_rxns
from set_up_grasp_models.set_up_models.set_up_meas_rates import _get_meas_fluxes, _set_up_meas_rates


def get_stoic(file_in: str) -> tuple:
    """
    From a text file with the reactions in the model, set up a dataframe with the transposed stoichiometric matrix.

    Args:
        file_in: path to plain text file with the model reactions.

    Returns:
        A pandas dataframe with transposed stoichiometric matrix, a list with reaction strings, a list with metabolites
        order, and a list with reactions order.
    """
    model = import_model_from_plaintext(file_in)
    rxn_list = model.to_string().split('\n')
    mets_order = list(model.metabolites.keys())
    rxns_order = list(model.reactions.keys())

    stoic_df = pd.DataFrame(model.stoichiometric_matrix(), columns=rxns_order, index=mets_order)
    stoic_df = stoic_df.transpose()
    stoic_df.index.name = 'rxn ID'

    return stoic_df, rxn_list, mets_order, rxns_order


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
        A pandas dataframe with tranposed stoichiometric matrix, a list with metabolites order, a list with reactions
        order, a list with exchange reactions to remove, and a list with external metabolites to remove.
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


def _add_general_sheet(writer, base_df: pd.DataFrame, base_excel_file: str, model_name: str):

    try:
        general_df = base_df['general']
    except KeyError:
        raise KeyError(f'The base excel file {base_excel_file} must contain a sheet named \'general\'')

    general_df.iloc[0, 0] = model_name
    general_df.to_excel(writer, sheet_name='general')

    return writer


def _add_stoic_sheet(writer, file_in_stoic: str) -> tuple:

    stoic_df, rxn_list, mets_order, rxns_order = get_stoic(file_in_stoic)
    stoic_df.to_excel(writer, sheet_name='stoic')

    return writer, rxn_list, mets_order, rxns_order


def _add_thermo_mets_sheet(writer, base_df: pd.DataFrame, file_in_mets_conc: str, mets_order: list, mets_orient: str):

    if file_in_mets_conc:
        mets_conc_df = _get_mets_conc(file_in_mets_conc, mets_order, orient=mets_orient)
    else:
        mets_conc_df = None

    thermo_mets_df, measured_mets = _set_up_thermo_mets(base_df, mets_order, mets_conc_df)
    thermo_mets_df.to_excel(writer, sheet_name='thermoMets')

    return writer, mets_conc_df, measured_mets


def _add_mets_sheet(writer, base_df: pd.DataFrame, mets_order: list, measured_mets: list):

    columns = ['Metabolite name', 'balanced?']
    mets_df = pd.DataFrame(index=mets_order, columns=columns, data=np.zeros([len(mets_order), len(columns)]))
    mets_df.index.name = 'metabolite ID'

    if 'mets' in base_df.keys():
        index_intersection = set(base_df['mets'].index.values).intersection(mets_df.index.values)
        mets_df.loc[index_intersection, :] = base_df['mets'].loc[index_intersection, :]

    mets_df.to_excel(writer, sheet_name='mets')

    return writer


def _add_rxns_sheet(writer, base_df: pd.DataFrame, rxns_order: list):

    columns = ['reaction name', 'transport reaction?', 'isoenzymes']
    rxns_df = pd.DataFrame(index=rxns_order, columns=columns, data=np.zeros([len(rxns_order), len(columns)]))
    rxns_df.index.name = 'reaction ID'

    if 'rxns' in base_df.keys():
        index_intersection = set(base_df['rxns'].index.values).intersection(rxns_df.index.values)
        rxns_df.loc[index_intersection, :] = base_df['rxns'].loc[index_intersection, :]
    rxns_df.to_excel(writer, sheet_name='rxns')

    return writer


def _add_pool_const_sheet(writer, base_df: pd.DataFrame, mets_order: list):

    pool_const_df = pd.DataFrame(index=mets_order)
    pool_const_df.index.name = 'metabolite ID'

    if 'poolConst' in base_df.keys():
        index_intersection = set(base_df['poolConst'].index.values).intersection(pool_const_df.index.values)
        pool_const_df.loc[index_intersection, :] = base_df['poolConst'].loc[index_intersection, :]

    pool_const_df.to_excel(writer, sheet_name='poolConst')

    return writer


def _add_thermo_ineq_constraints_sheet(writer, base_df: pd.DataFrame, mets_order: list):

    thermo_ineq_constraints_df = pd.DataFrame(index=mets_order)
    thermo_ineq_constraints_df.index.name = 'metabolite ID'

    if 'thermo_ineq_constraints' in base_df.keys():
        index_intersection = set(base_df['thermo_ineq_constraints'].index.values).intersection(
            thermo_ineq_constraints_df.index.values)
        thermo_ineq_constraints_df.loc[index_intersection, :] = base_df['thermo_ineq_constraints'].loc[
                                                                index_intersection, :]
    thermo_ineq_constraints_df.to_excel(writer, sheet_name='thermo_ineq_constraints')

    return writer


def _add_thermo_rxns(writer, base_df: pd.DataFrame, rxns_order: list, rxn_list: list, use_equilibrator: bool,
                     file_bigg_kegg_ids: str, pH: float, ionic_strength: float):

    thermo_rxns_df = _set_up_model_thermo_rxns(base_df, rxns_order, rxn_list, use_equilibrator, file_bigg_kegg_ids,
                                               pH, ionic_strength)
    thermo_rxns_df.to_excel(writer, sheet_name='thermoRxns')

    return writer


def _add_meas_rates_sheet(writer, base_df: pd.DataFrame, file_in_meas_fluxes: str, rxns_order: list, fluxes_orient: str):
    if file_in_meas_fluxes:
        rxn_fluxes_df = _get_meas_fluxes(file_in_meas_fluxes, rxns_order, orient=fluxes_orient)
    else:
        rxn_fluxes_df = None

    meas_rates_df = _set_up_meas_rates(base_df, rxn_fluxes_df, rxns_order)

    meas_rates_df.to_excel(writer, sheet_name='measRates')

    return writer


def _add_prot_data_sheet(writer, base_df: pd.DataFrame, rxns_order: list):
    columns = ['lower_bound', 'mean', 'upper_bound']
    prot_data_df = pd.DataFrame(index=rxns_order, columns=columns, data=np.tile(np.array([0.99, 1.00, 1.01]),
                                                                                (len(rxns_order), 1)))
    prot_data_df.index.name = 'reaction/enzyme ID'

    if 'protData' in base_df.keys():
        index_intersection = set(base_df['protData'].index.values).intersection(prot_data_df.index.values)
        prot_data_df.loc[index_intersection, :] = base_df['protData'].loc[index_intersection, :]

    prot_data_df.to_excel(writer, sheet_name='protData')

    return writer


def _add_mets_data_sheet(writer, base_df: pd.DataFrame, mets_order: list, mets_conc_df: pd.DataFrame):

    mets_data_df = _set_up_mets_data(base_df, mets_order, mets_conc_df)
    mets_data_df.to_excel(writer, sheet_name='metsData')

    return writer


def _add_kinetics_sheet(writer, base_df: pd.DataFrame, rxns_order: list):

    columns = ['kinetic mechanism', 'substrate order', 'product order', 'promiscuous', 'inhibitors',
               'activators', 'negative effectors', 'positive effectors', 'allosteric', 'subunits',
               'mechanism_refs_type', 'mechanism_refs', 'inhibitors_refs_type', 'inhibitors_refs',
               'activators_refs_type', 'activators_refs', 'negative_effectors_refs_type', 'negative_effectors_refs',
               'positive_effectors_refs_type', 'positive_effectors_refs', 'subunits_refs_type', 'subunits_refs',
               'comments']
    kinetics_df = pd.DataFrame(index=rxns_order, columns=columns, data=np.zeros([len(rxns_order), len(columns)]))
    kinetics_df.index.name = 'reaction ID'

    if 'kinetics1' in base_df.keys():
        index_intersection = set(base_df['kinetics1'].index.values).intersection(kinetics_df.index.values)
        kinetics_df.loc[index_intersection, :] = base_df['kinetics1'].loc[index_intersection, :]

    kinetics_df.to_excel(writer, sheet_name='kinetics1')

    return writer


def set_up_model(model_name: str, file_in_stoic: str, base_excel_file: str, file_out: str,
                 use_equilibrator: bool = False, pH: float = 7.0, ionic_strength: float = 0.1,
                 file_bigg_kegg_ids: str = None, file_in_mets_conc: str = None, mets_orient: str = 'columns',
                 file_in_meas_fluxes: str = None, fluxes_orient: str = 'columns', file_in_prot_ranges: str = None):
    """
    Sets up the excel input model file template. A base excel file must be given. This file must contain at least
    the general sheet, for that one can use the file 'GRASP_general.xlsx' in base_files. In this case an excel
    file with all fields to be filled is generated.

    If a base excel file with some of the sheets already filled or partially filled is available then whatever fields
    are already filled will be copied to the output model file.

    For thermoRxns, if use_equilibrator is set to True, it gets the standard Gibbs energies from eQuilibrator.

    If file_in_mets_conc is specified, it takes the metabolite concentrations from that file to fill in thermoMets
    and metsData. Metabolite names must have the form metBiggID_compartmentBiggID.
    The file must have either:
     - the metabolite names in the rows and two columns named average and stdev (set mets_orient to 'rows')
     - the metabolite names in the columns and two rows named average and stdev (set mets_orient to 'columns', the default)


    Args:
        model_name: name for the model.
        file_in_stoic: path to plain text file with reactions in the model.
        base_excel_file: path to the excel file to be used as a base.
        file_out: path to the output file.
        use_equilibrator: flag determining whether or not to get the standard Gibbs energies from eQuilibrator.
        pH: pH value to use to get the standard Gibbs energies from eQuilibrator.
        ionic_strength: ionic strength value to use to get the standard Gibbs energies from eQuilibrator.
        file_bigg_kegg_ids: path to the file containing the metabolites mapping from BiGG to KEGG ids.
        file_in_mets_conc: path to excel file containing metabolites concentrations.
        mets_orient: string specifying the orientation of metabolite concentrations, either 'rows' or 'columns'.
        file_in_meas_fluxes: path to excel file containing measured fluxes (not in use atm).
        fluxes_orient: string specifying the orientation of measured fluxes, either 'rows' or 'columns'.
        file_in_prot_ranges: path to excel file containing protein concentrations (not in use atm).

    Returns:
        None
    """

    writer = pd.ExcelWriter(file_out, engine='xlsxwriter')

    base_df = pd.read_excel(base_excel_file, index_col=0, header=0, sheet_name=None)

    writer = _add_general_sheet(writer, base_df, base_excel_file, model_name)

    writer, rxn_list, mets_order, rxns_order = _add_stoic_sheet(writer, file_in_stoic)

    writer, mets_conc_df, measured_mets = _add_thermo_mets_sheet(writer, base_df, file_in_mets_conc, mets_order,
                                                                 mets_orient)

    writer = _add_mets_sheet(writer, base_df, mets_order, measured_mets)

    writer = _add_rxns_sheet(writer, base_df, rxns_order)

    writer = _add_pool_const_sheet(writer, base_df, mets_order)

    writer = _add_thermo_ineq_constraints_sheet(writer, base_df, mets_order)

    writer = _add_thermo_rxns(writer, base_df, rxns_order, rxn_list, use_equilibrator, file_bigg_kegg_ids, pH,
                              ionic_strength)

    writer = _add_meas_rates_sheet(writer, base_df, file_in_meas_fluxes, rxns_order, fluxes_orient)

    writer = _add_prot_data_sheet(writer, base_df, rxns_order)

    writer = _add_mets_data_sheet(writer, base_df, mets_order, mets_conc_df)

    writer = _add_kinetics_sheet(writer, base_df, rxns_order)

    writer.save()

import pandas as pd
import numpy as np
import re


def set_up_rxns(file_in_base, rxns_order, ex_rxns_to_remove):
    """
    Given the base GRASP input excel file, removes the inactive exchange reactions and sets the order consistent with
         the stoichiometric matrix.

    :param file_in_base: path to base GRASP input excel file
    :param rxns_order: order of reactions in the stoichiometric matrix
    :param ex_rxns_to_remove: list of inactive exchange reactions
    :return:
        rxns_base_df:  the dataframe for the rxns excel sheet.
    """

    rxns_base_df = pd.read_excel(file_in_base, sheet_name='rxns', index_col=0)
    rxns_base_df = rxns_base_df.drop(ex_rxns_to_remove, axis=0)
    rxns_base_df = rxns_base_df.reindex(index=rxns_order)
    print(rxns_base_df)

    return rxns_base_df


def set_up_thermo_rxns(file_in_base, rxns_order, ex_rxns):
    """
     Given the base GRASP input excel file, adds the exchange reactions Gibbs energies.

    :param file_in_base:
    :param rxns_order:
    :param ex_rxns:
    :return:
    """

    thermo_rxns_df = pd.read_excel(file_in_base, sheet_name='thermoRxns', index_col=0)

    for ex_rxn in ex_rxns:
        if ex_rxn in ex_rxns:
            thermo_rxns_df.loc[ex_rxn] = [-10, 5]

    thermo_rxns_df = thermo_rxns_df.reindex(index=rxns_order)
    return thermo_rxns_df


def set_up_ex_rates(rxn_order, file_in_ex_fluxes, map_met_abbreviation, time_point, replicate, only_EX=True):

    n_rxns = len(rxn_order)

    ex_rates_df = pd.DataFrame(data=np.zeros((n_rxns, 4)), index=list(rxn_order),
                               columns=['vref_mean', 'vref_std', 'vexp1_mean', 'vexp1_std'])

    if only_EX:
        ex_rates_df = ex_rates_df.filter(regex='EX_', axis=0)

    ex_fluxes = pd.read_csv(file_in_ex_fluxes, index_col=0)

    ex_fluxes.index = ex_fluxes['Metabolite']

    ex_fluxes = ex_fluxes[ex_fluxes['Replicate'] == replicate]
    ex_fluxes = ex_fluxes.filter(regex=''.join(['_t', str(time_point), '$']))

    ex_fluxes.columns = ['vref_mean', 'vref_std']
    ex_fluxes['vexp1_mean'] = ex_fluxes['vref_mean']
    ex_fluxes['vexp1_std'] = ex_fluxes['vref_std']

    ex_fluxes.index = map(lambda x: '_'.join(['EX', re.findall('(\w+)_\w', map_met_abbreviation[x])[0]]), ex_fluxes.index.values)
    ex_rates_df.update(ex_fluxes)
    ex_rates_df.index.name = 'Fluxes (umol/gCDW/h)'


    # remove zero fluxes
    ex_rates_df = ex_rates_df[(ex_rates_df.T != 0).any()]
    ex_rates_df = ex_rates_df * 10**6  # convert to micro mol

    ex_rxns = ex_rates_df.index.values

    # get metabolites involved in exchange reactions
    ex_mets = set(map(lambda x: x[3:] + '_e', ex_rxns))

    print(ex_rates_df)
    return ex_rates_df, ex_rxns, ex_mets


def set_up_kinetics(file_in_base, rxns_order, ex_rxns):

    kinetics_base_df = pd.read_excel(file_in_base, sheet_name='kinetics1', index_col=0)

    for ex_rxn in ex_rxns:
        if ex_rxn in ex_rxns:
            kinetics_base_df.loc[ex_rxn] = ['massAction', np.nan,  np.nan, np.nan, np.nan, np.nan, np.nan, 0, 1, 'Modeled as mass action']
    kinetics_base_df = kinetics_base_df.reindex(index=rxns_order)
    print(kinetics_base_df)
    return kinetics_base_df




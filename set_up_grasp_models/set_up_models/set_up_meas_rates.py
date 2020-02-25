import re

import numpy as np
import pandas as pd


def _set_up_meas_rates(base_df, rxn_fluxes_df, rxns_order):
    """
    Given the base excel input file, the list of reactions in the model and a dataframe with reaction flux averages
    and respective stdev, fills in the measRates sheet.
    First fills in fluxes from rxn_fluxes_df and then from the base_df.
    Default values for measRates are [0, 0].

    Args:
        base_df: dict representing the base input excel file.
        rxn_fluxes_df: dataframe with reaction flux concentrations averages and respective stdev. Must have
                       a column named 'vref_mean' and another named 'vref_std'.
        rxns_order: list of reactions in the model.

    Returns:
        measRates dataframe.
    """
    columns = ['vref_mean (mmol/L/h)', 'vref_std (mmol/L/h)', 'vref_mean (mmol/L/h)', 'vref_std (mmol/L/h)']
    meas_rates_df = pd.DataFrame(index=rxns_order, columns=columns, data=np.zeros([len(rxns_order), len(columns)]))
    meas_rates_df.index.name = 'reaction ID'

    if rxn_fluxes_df is not None:
        try:
            meas_rates_df.loc[rxn_fluxes_df.index.values, 'vref_mean (mmol/L/h)'] = rxn_fluxes_df.loc[
                rxn_fluxes_df.index.values, 'vref_mean']
            meas_rates_df.loc[rxn_fluxes_df.index.values, 'vref_std (mmol/L/h)'] = rxn_fluxes_df.loc[
                rxn_fluxes_df.index.values, 'vref_std']
        except KeyError:
            raise KeyError(
                'The reaction IDs in the reaction fluxes dataframe do not match the reaction IDs in the rxns_order variable.')

    if 'measRates' in base_df.keys():
        index_intersection = set(base_df['measRates'].index.values).intersection(meas_rates_df.index.values)
        meas_rates_df.loc[index_intersection, :] = base_df['measRates'].loc[index_intersection, :]

    return meas_rates_df


def _get_meas_fluxes(file_in_meas_fluxes: str, rxns_order: list, orient: str = 'columns') -> pd.DataFrame:
    """
    Given an excel file with the measured flux values and the list of reactions in the model, it returns
    a dataframe with only the fluxes of the reactions in the model: average and respective standard
    deviation.
    The reaction names in the excel file with measured flux values are not expected to start with R_

    The file must have either:
     - the reaction names in the rows and two columns named vref_mean and vref_std (set orient to 'rows')
     - the reaction names in the columns and two rows named vref_mean and vref_std (set orient to 'columns', the default)

    Args:
        file_in_meas_fluxes: path to file with measured fluxes.
        rxns_order: list of reactions in the model.
        orient: whether reaction names are in columns (default) or in the rows.

    Returns:
        Dataframe with reaction fluxes and respective standard deviation; reaction names on the rows,
        average and stdev on the columns.
    """

    rxn_fluxes = pd.read_excel(file_in_meas_fluxes, index_col=0, header=0)

    if orient == 'rows':
        rxn_fluxes = rxn_fluxes.transpose()

    if 'vref_mean' not in rxn_fluxes.index.values or 'vref_std' not in rxn_fluxes.index.values:
        raise IndexError(f'No rows named vref_mean and vref_std found in the first sheet of {file_in_meas_fluxes}.')

    rxns_list = [re.findall('R?_?(\S+)', rxn)[0] for rxn in rxns_order]
    rxn_fluxes = rxn_fluxes.loc[['vref_mean', 'vref_std'], rxn_fluxes.columns.isin(rxns_list)]

    rxn_fluxes = rxn_fluxes.transpose()
    rxn_fluxes.index = [f'R_{rxn}' for rxn in rxn_fluxes.index.values]

    return rxn_fluxes

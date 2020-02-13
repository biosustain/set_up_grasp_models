import re

import numpy as np
import pandas as pd


def _set_up_mets_data(base_df: pd.DataFrame, mets_list: list, mets_conc_df: pd.DataFrame) -> pd.DataFrame:
    """
    Given the base excel input file, the list of metabolites in the model and a dataframe with metabolite
    concentrations averages and respective stdev, fills in the metsData sheet.
    Default values for metsData are [0.99, 1.00, 1.01].

    Args:
        base_df: dict representing the base input excel file.
        mets_list: list of metabolites in the model.
        mets_conc_df: dataframe with metabolite concentrations averages and respective stdev. Must have
                      a column named 'average' and another named 'stdev'.

    Returns:
        metsData dataframe.
    """

    columns = ['lower_bound', 'mean', 'upper_bound']
    mets_data_df = pd.DataFrame(index=mets_list, columns=columns, data=np.tile(np.array([0.99, 1.00, 1.01]),
                                                                               (len(mets_list), 1)))
    mets_data_df.index.name = 'metabolite ID'
    if 'metsData' in base_df.keys():
        index_intersection = set(base_df['metsData'].index.values).intersection(mets_data_df.index.values)
        mets_data_df.loc[index_intersection, :] = base_df['metsData'].loc[index_intersection, :]

    if mets_conc_df is not None:
        mets_conc_df['lb'] = (mets_conc_df['average'] - mets_conc_df['stdev']) / mets_conc_df['average']
        mets_conc_df['ub'] = (mets_conc_df['average'] + mets_conc_df['stdev']) / mets_conc_df['average']
        mets_conc_df = mets_conc_df.dropna()

        mets_data_df.loc[mets_conc_df.index.values, 'lower_bound'] = mets_conc_df.loc[mets_conc_df.index.values, 'lb']
        mets_data_df.loc[mets_conc_df.index.values, 'upper_bound'] = mets_conc_df.loc[mets_conc_df.index.values, 'ub']

    return mets_data_df


def _set_up_thermo_mets(base_df: pd.DataFrame, mets_list: list, mets_conc_df: pd.DataFrame) -> tuple:
    """
    Given the base excel input file, the list of metabolites in the model and a dataframe with metabolite
    concentrations averages and respective stdev, fills in the thermoMets sheet.
    First fills in concentrations from mets_conc_df and then from the base_df.
    Default values for thermoMets are [10^-12, 10^-1] M.

    Args:
        base_df: dict representing the base input excel file.
        mets_list: list of metabolites in the model.
        mets_conc_df: dataframe with metabolite concentrations averages and respective stdev. Must have
                                     a column named 'average' and another named 'stdev'.

    Returns:
        thermoMets dataframe and list of measured metabolites.
    """

    columns = ['min (M)', 'max (M)']
    thermo_mets_df = pd.DataFrame(index=mets_list, columns=columns, data=np.tile(np.array([10 ** -12, 10 ** -1]),
                                                                                 (len(mets_list), 1)))
    thermo_mets_df.index.name = 'metabolite ID'

    if mets_conc_df is not None:
        mets_conc_df['min'] = mets_conc_df['average'] - mets_conc_df['stdev']
        mets_conc_df['max'] = mets_conc_df['average'] + mets_conc_df['stdev']

        thermo_mets_df.loc[mets_conc_df.index.values, 'min (M)'] = mets_conc_df.loc[mets_conc_df.index.values, 'min']
        thermo_mets_df.loc[mets_conc_df.index.values, 'max (M)'] = mets_conc_df.loc[mets_conc_df.index.values, 'max']

        measured_mets = mets_conc_df.index.values
    else:
        measured_mets = []

    if 'thermoMets' in base_df.keys():
        index_intersection = set(base_df['thermoMets'].index.values).intersection(thermo_mets_df.index.values)
        thermo_mets_df.loc[index_intersection, :] = base_df['thermoMets'].loc[index_intersection, :]

    return thermo_mets_df, measured_mets


def _get_mets_conc(file_in_met_conc: str, mets_list: list, orient: str = 'columns') -> pd.DataFrame:
    """
    Given an excel file with the metabolite concentrations and the list of metabolites in the model, it returns
    a dataframe with only the concentrations of the metabolites in the model: average and respective standard
    deviation.

    The file must have either:
     - the metabolite names in the rows and two columns named average and stdev (set orient to 'rows')
     - the metabolite names in the columns and two rows named average and stdev (set orient to 'columns', the default)

    Args:
        file_in_met_conc: path to file with metabolite concentrations.
        mets_list: list of metabolites in the model.
        orient: whether metabolite names are in columns (default) or in the rows.

    Returns:
        Dataframe with metabolite concentrations and respective standard deviation; metabolite names on the rows,
        average and stdev on the columns.
    """

    mets_conc_df = pd.read_excel(file_in_met_conc, index_col=0, header=0)

    if orient == 'rows':
        mets_conc_df = mets_conc_df.transpose()

    if 'average' not in mets_conc_df.index.values or 'stdev' not in mets_conc_df.index.values:
        raise IndexError(f'No rows named average and stdev found in the first sheet of {file_in_met_conc}.')

    mets_list = [re.findall('m?_?(\S+)', met)[0] for met in mets_list]
    mets_conc_df = mets_conc_df.loc[['average', 'stdev'], mets_conc_df.columns.isin(mets_list)]

    mets_conc_df = mets_conc_df.transpose()
    mets_conc_df.index = [f'm_{met}' for met in mets_conc_df.index.values]

    return mets_conc_df

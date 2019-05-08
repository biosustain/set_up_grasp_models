#from src.set_up_grasp_models.misc import get_stoic
from src.set_up_grasp_models.set_up_rates import set_up_ex_rates
import pandas as pd
import numpy as np


def set_up_mets(file_in_base_model, mets_order, ex_mets_to_remove):

    mets_base_df = pd.read_excel(file_in_base_model, sheet_name='mets', index_col=0)
    mets_base_df = mets_base_df.drop(ex_mets_to_remove)
    mets_base_df = mets_base_df.reindex(mets_order)

    return mets_base_df


def set_up_thermo_mets(mets_order, file_in_met_ranges, map_met_abbreviation, met_lb=10**-12, met_ub=10**-8):
    n_mets = len(mets_order)

    lb = np.repeat(met_lb, n_mets)
    ub = np.repeat(met_ub, n_mets)
    thermo_mets_df = pd.DataFrame(data=np.matrix([lb, ub]).transpose(), index=list(mets_order), columns=['min (M)', 'max (M)'])

    met_ranges = pd.read_csv(file_in_met_ranges, index_col=0)
    met_ranges = met_ranges.drop('metabolite.1', axis=1)

    # to be deleted
    met_ranges.columns = ['min (M)', 'max (M)', 'lb normalized', 'ub normalized']

    met_ranges['min (M)'][met_ranges['min (M)'] < met_lb] = met_lb
    met_ranges['max (M)'][met_ranges['max (M)'] < met_ub] = met_ub

    met_ranges.index = map(lambda x: map_met_abbreviation[x], met_ranges.index.values)

    thermo_mets_df.update(met_ranges)
    thermo_mets_df.index.name = 'met'
    print(thermo_mets_df)

    try:
        assert np.all(thermo_mets_df['min (M)'].values < thermo_mets_df['max (M)'].values)

    except AssertionError:
        print('Some metabolite lower bound is larger than the respective upper bound')
        print('Lower bounds:')
        print(thermo_mets_df['min (M)'].values)
        print('Upper bounds:')
        print(thermo_mets_df['max (M)'].values)

        return None

    return thermo_mets_df


def set_up_mets_data(mets_order, file_in_met_ranges, map_met_abbreviation, met_lb=0.99, met_ub=1.01):

    #stoic_df, mets_order, rxn_order = get_stoic(file_in_base_model)
    n_mets = len(mets_order)

    lb = np.repeat(met_lb, n_mets)
    mean = np.repeat(1, n_mets)
    ub = np.repeat(met_ub, n_mets)
    mets_data_df = pd.DataFrame(data=np.matrix([lb, mean, ub]).transpose(), index=list(mets_order),
                                columns=['MBo10_LB2 (M)', 'MBo10_meas2', 'MBo10_UB2 (M)'])

    met_ranges = pd.read_csv(file_in_met_ranges, index_col=0)
    met_ranges = met_ranges.drop('metabolite.1', axis=1)

    # to be deleted
    met_ranges.columns = ['min (M)', 'max (M)', 'MBo10_LB2 (M)', 'MBo10_UB2 (M)']
    met_ranges['MBo10_LB2 (M)'][(met_ranges['MBo10_LB2 (M)'] == 0) & (met_ranges['MBo10_UB2 (M)'] == 0)] = met_lb
    met_ranges['MBo10_UB2 (M)'][met_ranges['MBo10_UB2 (M)'] == 0] = met_ub

    met_ranges.index = map(lambda x: map_met_abbreviation[x], met_ranges.index.values)

    mets_data_df.update(met_ranges)
    mets_data_df.index.name = 'met'
    print(mets_data_df)

    try:
        assert np.all(mets_data_df['MBo10_LB2 (M)'].values < mets_data_df['MBo10_UB2 (M)'].values)

    except AssertionError:
        print('Some metabolite lower bound is larger than the respective upper bound')
        print('Lower bounds:')
        print(mets_data_df['MBo10_LB2 (M)'].values)
        print('Upper bounds:')
        print(mets_data_df['MBo10_UB2 (M)'].values)

        return None


    return mets_data_df



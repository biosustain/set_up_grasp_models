import re

import numpy as np
import pandas as pd


def set_up_proteomics(rxn_order, ex_rxns, file_in_prot_ranges, map_prot_abbreviation, time_point, replicate, prot_lb = 0.99, prot_ub=1.01):

    in_rxns = list(filter(lambda x: not x.startswith('EX_'), rxn_order))
    n_rxns = len(in_rxns)

    lb = np.repeat(prot_lb, n_rxns)
    mean = np.repeat(1, n_rxns)
    ub = np.repeat(prot_ub, n_rxns)
    prot_data_df = pd.DataFrame(data=np.matrix([lb, mean, ub]).transpose(), index=list(in_rxns), columns=['MBo10_LB2', 'MBo10_meas2', 'MBo10_UB2'])

    prot_data_df.index.name = 'enzyme/rxn'
    prot_ranges = pd.read_csv(file_in_prot_ranges, index_col=0)
    prot_ranges.index = [map_prot_abbreviation[prot] for prot in prot_ranges['PG,ProteinAccessions']]


    prot_ranges = prot_ranges.filter(regex=''.join(['P', str(time_point+1), ' ']))

    # to be deleted
    prot_ranges.columns = ['MBo10_LB2', 'MBo10_meas2', 'MBo10_UB2']
    rxn_set_1 = list(filter(lambda x: re.search('_', x), in_rxns))
    rxn_set_2 = list(filter(lambda x: not re.search('_', x), in_rxns))
    promiscuous_rxns  = set([rxn.split('_')[0] for rxn in rxn_set_1]).intersection(rxn_set_2)

    for rxn in promiscuous_rxns:
        prot_ranges.loc[rxn] = prot_ranges.loc[rxn.split('_')[0]].values
    prot_ranges = prot_ranges.reindex(in_rxns)

    prot_data_df.update(prot_ranges)
    for rxn in ex_rxns:
        prot_data_df.loc[rxn] = [0.99, 1.00, 1.01]

    print(prot_data_df)

    return prot_data_df


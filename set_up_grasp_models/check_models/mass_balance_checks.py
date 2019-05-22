
def check_flux_balance(data_dict: dict) -> bool:
    """
    When all fluxes are specified in the measRates sheet, check if all metabolites are mass balanced (well, the ones
    that are marked as balanced in the mets sheet).
    If everything is fine flag is 0, otherwise it is set to 1.

    Args:
        data_dict (dict): a dictionary that represents the excel file with the GRASP model

    Returns:
        bool: whether or not all metabolites mass is balanced

    """

    print('\nChecking if the fluxes for each metabolite production/consumptions add up to zero.\n')

    flag = False
    flux_df = data_dict['measRates']
    mets_df = data_dict['mets']
    stoic_df = data_dict['stoic']

    if len(stoic_df.index) == len(flux_df.index):

        stoic_df.index = stoic_df['rxn ID']
        del stoic_df['rxn ID']

        met_in_rxns = dict()
        for col in stoic_df.columns:
            rxn_list = stoic_df.loc[stoic_df[col].ne(0), col]
            met_in_rxns[col] = rxn_list.to_dict()

        mets_df.index = mets_df['ID']
        balanced_mets = set(mets_df.loc[mets_df['balanced?'].eq(1), 'balanced?'].index.values)

        flux_df.index = flux_df[flux_df.columns[0]]
        del flux_df[flux_df.columns[0]]
        mean_col = flux_df.columns[0]

        for met in met_in_rxns.keys():

            flux_balance = sum([met_in_rxns[met][key] * flux_df.loc[key, mean_col] for key in met_in_rxns[met].keys()])

            if flux_balance != 0 and met in balanced_mets:
                print(f'The flux for {met} is not balanced. The difference in flux is {flux_balance}')
                flag = True
            elif flux_balance == 0 and met not in balanced_mets:
                print(f'{met} should be in balanced mets')
                flag = True

        if flag is False:
            print('Everything seems to be OK.')

    else:
        print('Not all fluxes are specified in measRates.\n')


    return flag


def check_balanced_metabolites(data_dict: dict) -> bool:
    """
    Checks if metabolites that are both consumed and produced in the stoichiometric matrix are marked as balanced and
    the other way around. Checking for mass balances is more accurate though.
    If everything is fine flag is 0, otherwise it is set to 1.

    Args:
        data_dict (dict): a dictionary that represents the excel file with the GRASP model

    Returns:
        bool: whether or not metabolites are marked balanced/fixed correctly

    """

    print('\nChecking if metabolites are both consumed and produced in the stoichiometric matrix, and if',
          'so checks if they are marked as balanced in the mets sheet. However, the metabolite might be',
          'balanced/not balanced anyways depending on the flux of the reactions that consume/produce it,',
          'so take this with a grain of salt.\n')

    flag = False
    stoic_df = data_dict['stoic']
    stoic_df.index = stoic_df['rxn ID']
    stoic_df = stoic_df.drop('rxn ID', axis=1)
    mets_df = data_dict['mets']

    for i, met in enumerate(stoic_df.columns):
        if stoic_df[met].gt(0).any() and stoic_df[met].lt(0).any():
            if mets_df['balanced?'][i] == 0:
                print(f'{met} is marked as not balanced but it seems to be balanced.')
                flag = True
        else:
            if mets_df['balanced?'][i] == 1:
                print(f'{met} is marked as balanced but it does not seem to be balanced.')
                flag = True
            if mets_df['fixed?'][i] == 0:
                print(f'{met} is not set as constant but maybe it should, since it does not seem to be balanced.')
                flag = True

    if flag is False:
        print('Everything seems to be OK.')

    return flag
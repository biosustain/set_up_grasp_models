import numpy as np


def check_met_rxn_order(data_dict: dict) -> bool:
    """
    Given the excel file as argument, checks if the order of reactions and metabolites in all sheets is consistent
    with the order in the stoichiometry matrix.
    If everything is fine flag is 0, otherwise it is set to 1.

    Args:
        data_dict (dict): a dictionary that represents the excel file with the GRASP model.

    Returns:
        flag (bool): whether or not reactions and metabolites order in the different sheets are consistent

    """

    print('\nChecking if the order of reactions and metabolites is the same in all excel sheets.\n')

    flag = False
    rxn_list = data_dict['stoic'].iloc[:, 0].values
    met_list = data_dict['stoic'].columns.values[1:]
    flux_df = data_dict['measRates']

    met_sheets = {'mets', 'poolConst', 'thermo_ineq_constraints', 'thermoMets', 'metsData'}
    rxn_sheets = {'rxns', 'splitRatios', 'thermoRxns', 'protData'}

    for key in list(data_dict.keys())[2:]:

        id_list = data_dict[key].iloc[:, 0].values

        if key in met_sheets:

            if len(id_list) != len(met_list):
                print(f'Metabolite list in sheet {key} doesn\'t have the same length of the list in the stoichiometric'
                      f' matrix')
                flag = True

            else:
                met_bool = np.equal(id_list, met_list)
                met_bool = all(met_bool) if isinstance(met_bool, np.ndarray) else met_bool

                if not met_bool:
                    print(f'Metabolite list in sheet {key} doesn\'t match the list in the stoichiometric matrix.')
                    print(f'Current list:\n {id_list}')
                    print(f'Metabolite list in stoichiometric matrix:\n {met_list}\n')
                    flag = True

        elif key in rxn_sheets or key.startswith('kinetics') or \
                (key == 'measRates' and len(rxn_list) == len(flux_df.index)):

            if len(id_list) != len(rxn_list):
                print(f'Reaction list in sheet {key} doesn\'t have the same length of the list in the stoichiometric'
                      f' matrix')
                flag = True

            else:
                rxn_bool = np.equal(id_list, rxn_list)
                rxn_bool = all(rxn_bool) if isinstance(rxn_bool, np.ndarray) else rxn_bool

                if not rxn_bool:
                    print(f'Reaction list in sheet {key} doesn\'t match the list in the stoichiometric matrix.')
                    print(f'Current list:\n {id_list}')
                    print(f'Reaction list in stoichiometric matrix:\n {rxn_list}\n')
                    flag = True

    if flag is False:
        print('Everything seems to be OK.\n')

    return flag


def _check_kinetics_column(kinetics_df: dict, col_name: str) -> bool:

    flag = False
    kinetics_df.columns = kinetics_df.columns.str.lower()
    col_data = kinetics_df[col_name].dropna()
    for row in col_data:
        try:
            if row.find(',') != -1 or row.find(';') != -1 or row.find('.') != -1:
                print(f'Make sure all metabolites are separated by a single space in column "{col_name}" row:\n {row}\n')
                flag = True

        except AttributeError:
            raise AttributeError('Make sure the columns in the kinetics sheet contain text and not numbers.')

    return flag


def check_kinetics_met_separators(data_dict: dict) -> bool:
    """
    Given the excel file as argument, in the kinetics sheet for columns where cells can have multiple values, makes
    sure these values are not separated by a comma, semi-colon, or dot.
    If everything is fine flag is 0, otherwise it is set to 1.

    Args:
        data_dict (dict): a dictionary that represents the excel file with the GRASP model.

    Returns:
        flag (bool): whether or not lists in the kinetics sheet are separated by a space

   """

    print('\nChecking if values are separated by a space in the kinetics sheet in columns order, promiscuous,',
          'inhibitors, activators, negative effector, and positive effector.\nIt looks for dots, commas, and',
          'semi-colons.\n')

    flag_list = []

    for key in list(data_dict.keys()):
        if key.startswith('kinetics'):
            flag = _check_kinetics_column(data_dict[key], 'substrate order')
            flag_list.append(flag)
            flag = _check_kinetics_column(data_dict[key], 'product order')
            flag_list.append(flag)
            flag = _check_kinetics_column(data_dict[key], 'promiscuous')
            flag_list.append(flag)
            flag = _check_kinetics_column(data_dict[key], 'inhibitors')
            flag_list.append(flag)
            flag = _check_kinetics_column(data_dict[key], 'activators')
            flag_list.append(flag)
            flag = _check_kinetics_column(data_dict[key], 'negative effector')
            flag_list.append(flag)
            flag = _check_kinetics_column(data_dict[key], 'positive effector')
            flag_list.append(flag)

    if not any(flag_list):
        print('Everything seems to be OK.\n')

    return any(flag_list)


def check_rxn_mechanism_order(data_dict: dict) -> bool:
    """
    Given the excel file as argument, it goes through the 'kinetic mechanism' column in the 'kinetics1' sheet
    and checks if hard coded mechanisms ('diffusion', 'freeExchange', 'fixedExchange', 'massAction') come before 
    enzymatic mechanisms. Also checks if 'fixedExchange' mechanisms are the very last ones. 
    
    Args:
        data_dict (dict): a dictionary that represents the excel file with the GRASP model.

    Returns:
        flag (bool): whether or not lists in the kinetics sheet are separated by a space
    """

    print('\nChecking if non enzymatic mechanisms come only after enzymatic ones and if fixedExchange is the ' +
          'very last one.\n')

    hard_coded_mechs = {'diffusion', 'freeExchange', 'fixedExchange', 'massAction'}
    kinetics_df = data_dict['kinetics1']
    flag = False
    mech_hard_coded = 0
    fixed_exchange = 0

    for i, mech in enumerate(kinetics_df['kinetic mechanism']):

        if mech_hard_coded == 1 and mech.strip() not in hard_coded_mechs:
            print(f'Enzymatic mechanism {mech} for reaction {kinetics_df.iloc[i][0]} ' +
                  f'should come before \'diffusion\', \'freeExchange\', \'fixedExchange\', \'massAction\'.')
            flag = True

        if fixed_exchange == 1 and mech.strip() != 'fixedExchange':
            print(f'Mechanism {mech} for reaction {kinetics_df.iloc[i][0]} should come before ' +
                  f'fixedExchange mechanisms.')
            flag = True

        if mech.strip() in hard_coded_mechs:
            mech_hard_coded = 1

        if mech.strip() == 'fixedExchange':
            fixed_exchange = 1

    return flag


def check_kinetics_subs_prod_order(data_dict: dict) -> bool:
    """
    Given a GRASP input excel file, check if the metabolite names in the substrate and product order columns in
    the kinetics sheet are valid, i.e. if they are indeed substrates and products of the respective reaction.
    Inactive metabolites are not accounted for.

    Args:
        data_dict (dict): a dictionary that represents the excel file with the GRASP model.

    Returns:
        flag (bool): whether or not lists in the kinetics sheet are separated by a space
    """

    print('\nChecking if the metabolite names in the substrate and product order columns in the kinetics sheet are '
          'valid, i.e., if they are indeed substrates and products of the respective reaction.\n')

    flag = False

    mets_df = data_dict['mets']
    mets_df.index = mets_df.iloc[:, 0]
    inactive_mets = set(mets_df[mets_df['active?'].eq(0)].index.values)

    stoic_df = data_dict['stoic']
    stoic_df.index = stoic_df.iloc[:, 0]
    stoic_df = stoic_df.drop(stoic_df.columns[0], axis=1)

    kinetics_df = data_dict['kinetics1']
    kinetics_df.index = kinetics_df.iloc[:, 0]

    kinetics_df.columns = kinetics_df.columns.str.lower()
    for rxn in kinetics_df.index:

        rxn_subs = set(stoic_df.loc[rxn][stoic_df.loc[rxn].lt(0)].index.values).difference(inactive_mets)
        rxn_prods = set(stoic_df.loc[rxn][stoic_df.loc[rxn].gt(0)].index.values).difference(inactive_mets)

        subs_order = kinetics_df.loc[rxn, 'substrate order']
        subs_set = set(subs_order.split()) if type(subs_order) is str else None

        if subs_set is not None and subs_set != rxn_subs:
            if len(subs_set.difference(rxn_subs)) > 0:
                print(f'The following metabolites in the substrate order column for reaction {rxn} are not part of '
                      f'the reaction substrates:\n{subs_set.difference(rxn_subs)}\n')
            elif len(rxn_subs.difference(subs_set)) > 0:
                print(f'The following reaction substrates are not part of the substrate order column for '
                      f'reaction {rxn} :\n{rxn_subs.difference(subs_set)}\n')
            flag = True

        prod_order = kinetics_df.loc[rxn, 'product order']
        prod_set = set(prod_order.split()) if type(prod_order) is str else None

        if prod_set is not None and prod_set != rxn_prods:
            if len(prod_set.difference(rxn_prods)) > 0:
                print(f'The following metabolites in the product order column for reaction {rxn} are not part of '
                      f'the reaction products:\n{prod_set.difference(rxn_prods)}\n')
            elif len(rxn_prods.difference(prod_set)) > 0:
                print(f'The following reaction products are not part of the product order column for '
                      f'reaction {rxn} :\n{rxn_prods.difference(prod_set)}\n')
            flag = True

    if not flag:
        print('Everything seems to be OK.\n')

    return flag
import numpy as np


def check_met_rxn_order(data_dict: dict) -> bool:
    """
    Given the excel file as argument, checks if the order of reactions and metabolites in all sheets is consistent
    with the order in the stoichiometry matrix.
    If everything is fine flag is 0, otherwise it is set to 1.

    Args:
        data_dict (dict): a dictionary that represents the excel file with the GRASP model.

    Returns:
        bool: whether or not reactions and metabolites order in the different sheets are consistent

    """

    print('\nChecking if the order of reactions and metabolites is the same in all excel sheets.\n')

    flag = False
    rxn_list = data_dict['stoic']['rxn ID'].values
    met_list = data_dict['stoic'].columns.values[1:]
    flux_df = data_dict['measRates']

    met_sheets = {'mets', 'poolConst', 'thermo_ineq_constraints', 'thermoMets', 'metsData'}
    rxn_sheets = {'rxns', 'splitRatios', 'thermoRxns', 'protData'}

    for key in list(data_dict.keys())[2:]:
        id_list = data_dict[key].iloc[:, 0].values

        if key in met_sheets:

            met_bool = np.equal(id_list, met_list)
            met_bool = all(met_bool) if isinstance(met_bool, np.ndarray) else met_bool

            if not met_bool:
                print(f'Metabolite list in sheet {key} doesn\'t match the list in the stoichiometry matrix.')
                print(f'Current list:\n {id_list}')
                print(f'Metabolite list in stoichiometric matrix:\n {met_list}\n')
                flag = True

        elif key in rxn_sheets or key.startswith('kinetics') or \
                (key == 'measRates' and len(rxn_list) == len(flux_df.index)):

            rxn_bool = np.equal(id_list, rxn_list)
            rxn_bool = all(rxn_bool) if isinstance(rxn_bool, np.ndarray) else rxn_bool

            if not rxn_bool:
                print(f'Reaction list in sheet {key} doesn\'t match the list in the stoichiometry matrix.')
                print(f'Current list:\n {id_list}')
                print(f'Reaction list in stoichiometric matrix:\n {rxn_list}\n')
                flag = True

    if flag is False:
        print('Everything seems to be OK.\n')

    return flag


def _check_kinetics_column(data_dict: dict, col_name: str) -> bool:

    flag = False
    col_data = data_dict[col_name].dropna()
    for row in col_data:
        if row.find(',') != -1 or row.find(';') != -1 or row.find('.') != -1:
            print(f'Make sure all metabolites are separated by a single space in column "{col_name}" row:\n {row}\n')
            flag = True

    return flag


def check_kinetics_met_separators(data_dict: dict) -> bool:
    """
    Given the excel file as argument, in the kinetics sheet for columns where cells can have multiple values, makes
    sure these values are not separated by a comma, semi-colon, or dot.
    If everything is fine flag is 0, otherwise it is set to 1.

    Args:
        data_dict (dict): a dictionary that represents the excel file with the GRASP model.

    Returns:
        bool: whether or not lists in the kinetics sheet are separated by a space

   """

    print('\nChecking if values are separated by a space in the kinetics sheet in columns order, promiscuous,',
          'inhibitors, activators, negative effector, and positive effector.\nIt looks for dots, commas, and',
          'semi-colons.\n')

    flag_list = []

    for key in list(data_dict.keys()):
        if key.startswith('kinetics'):
            flag = _check_kinetics_column(data_dict[key], 'order')
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

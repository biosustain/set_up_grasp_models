import pandas as pd


def import_stoic(file_in: str) -> tuple:
    """
    Gets the reaction strings from the stoichiometry matrix defined in the GRASP input models.

    Args:
        file_in (str): path to file containing the model

    Returns:
        tuple: metabolite list, reaction list, reaction strings list
   """

    data_df = pd.read_excel(file_in, sheet_name='stoic', index_col=0, header=0)
    data_df = data_df.fillna('')
    rxn_strings = []

    mets = data_df.columns.values
    rxns = data_df.index.values

    for row in data_df.index:

        subs_entries = data_df.loc[row][data_df.loc[row].lt(0)]
        sub_stoic_coeffs = subs_entries.values
        subs = subs_entries.index.values

        prod_entries = data_df.loc[row][data_df.loc[row].gt(0)]
        prod_stoic_coeffs = prod_entries.values
        prods = prod_entries.index.values

        subs_with_coeffs = [f'{str(abs(coef))} {met}' if abs(coef) != 1 else met for coef, met in zip(sub_stoic_coeffs, subs)]
        subs_part = ' + '.join(subs_with_coeffs)

        prods_with_coeffs = [f'{str(abs(coef))} {met}' if abs(coef) != 1 else met for coef, met in zip(prod_stoic_coeffs, prods)]
        prods_part = ' + '.join(prods_with_coeffs)

        rxn_string = ' <-> '.join([subs_part, prods_part])
        rxn_string = f'{row}: {rxn_string}'

        rxn_strings.append(rxn_string)

    return mets, rxns, rxn_strings


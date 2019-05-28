import pandas as pd


def reorder_reactions(data_dict: dict, rxn_list: list, file_out: str):
    """
    Given a dictionary representing a GRASP input excel and a list of reactions it reorders the reaction in
    all excel sheets that and writes the new reordered sheets to file_out

    Args:
        data_dict (dict): dictionary representing GRASP input excel file.
        rxn_list (list): list with the new reaction order.
        file_out (str): path to excel input file to be outputed.

    Returns:
        None
    """

    sheets_to_reorder = ['stoic', 'rxns', 'splitRatios', 'thermoRxns', 'measRates', 'protData', 'kinetics1']
    writer = pd.ExcelWriter(file_out, engine='xlsxwriter')

    for sheet in data_dict.keys():

        if sheet in sheets_to_reorder:
            if sheet == 'measRates' and len(data_dict[sheet].index) != len(data_dict['stoic'].index):
                meas_rates_rxns = [rxn for rxn in rxn_list if rxn in data_dict[sheet].index]
                ordered_sheet = data_dict[sheet].reindex(meas_rates_rxns)
            else:
                ordered_sheet = data_dict[sheet].reindex(rxn_list)

            ordered_sheet.to_excel(writer, sheet_name=sheet)

        else:
            data_dict[sheet].to_excel(writer, sheet_name=sheet)

    writer.save()

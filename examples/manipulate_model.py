import os

import pandas as pd

from set_up_grasp_models.set_up_models.manipulate_model import remove_spaces, reorder_reactions, rename_columns


# list with reaction order
rxn_list = ['TPH', 'DDC', 'AANAT', 'ASMT', 'DDC_tryptm', 'AANAT_tryptm', 'IN_trp',
            'EX_trp', 'EX_fivehtp', 'EX_nactsertn', 'EX_meltn', 'EX_nactryptm', 'EX_srtn']

# path to current model
data_dict = pd.read_excel(os.path.join('models', 'HMP2360_r0_t0_mech_order.xlsx'),
                          sheet_name=None, index_col=0)

# path to the model with re-ordered reactions
file_out = os.path.join('models', 'HMP2360_r0_t0_mech_order_fixed.xlsx')

# re-order reactions according to rxn_list
reorder_reactions(data_dict, rxn_list, file_out)


# remove any leading or trailing spaces in all string cells
remove_spaces(data_dict, file_out)

# renames columns names, so that they are standard and cause no problems with other functions
rename_columns(data_dict, file_out)


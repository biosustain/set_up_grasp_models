import os
import unittest

import pandas as pd

from set_up_grasp_models.set_up_models.manipulate_model import remove_spaces, reorder_reactions, rename_columns


class TestIO(unittest.TestCase):

    def setUp(self):
        this_dir, this_filename = os.path.split(__file__)
        self.test_folder = os.path.join(this_dir, 'test_files', 'test_set_up_models', 'manipulate_model')

    def test_reorder_reactions(self):
        true_res = pd.read_excel(os.path.join(self.test_folder, 'true_res_HMP2360_r0_t0_mech_order_fixed.xlsx'),
                                 sheet_name=None, index_col=0)

        rxn_list = ['TPH', 'DDC', 'AANAT', 'ASMT', 'DDC_tryptm', 'AANAT_tryptm', 'IN_trp',
                    'EX_trp', 'EX_fivehtp', 'EX_nactsertn', 'EX_meltn', 'EX_nactryptm', 'EX_srtn']
        data_dict = pd.read_excel(os.path.join(self.test_folder, 'HMP2360_r0_t0_mech_order.xlsx'),
                                  sheet_name=None, index_col=0)
        file_out = os.path.join(self.test_folder, 'HMP2360_r0_t0_mech_order_fixed.xlsx')

        reorder_reactions(data_dict, rxn_list, file_out)
        res = pd.read_excel(file_out, sheet_name=None, index_col=0)

        self.assertListEqual(list(true_res.keys()), list(res.keys()))
        for sheet in true_res.keys():
            self.assertTrue(true_res[sheet].equals(res[sheet]))

    def test_remove_spaces(self):
        true_res = pd.read_excel(os.path.join(self.test_folder, 'true_res_HMP2360_r0_t0_mech_spaces_fixed.xlsx'),
                                 sheet_name=None, index_col=0)

        data_dict = pd.read_excel(os.path.join(self.test_folder, 'HMP2360_r0_t0_mech_spaces.xlsx'),
                                  sheet_name=None, index_col=0)
        file_out = os.path.join(self.test_folder, 'HMP2360_r0_t0_mech_spaces_fixed.xlsx')

        remove_spaces(data_dict, file_out)
        res = pd.read_excel(file_out, sheet_name=None, index_col=0)

        self.assertListEqual(list(true_res.keys()), list(res.keys()))
        for sheet in true_res.keys():
            self.assertTrue(true_res[sheet].equals(res[sheet]))

    def test_rename_columns(self):
        true_res = pd.read_excel(os.path.join(self.test_folder, 'true_res_HMP2360_r0_t0_cols.xlsx'),
                                 sheet_name=None, index_col=0)

        data_dict = pd.read_excel(os.path.join(self.test_folder, 'HMP2360_r0_t0_cols.xlsx'),
                                  sheet_name=None, index_col=0)
        file_out = os.path.join(self.test_folder, 'HMP2360_r0_t0_cols_fixed.xlsx')

        rename_columns(data_dict, file_out)
        res = pd.read_excel(file_out, sheet_name=None, index_col=0)

        self.assertListEqual(list(true_res.keys()), list(res.keys()))
        for sheet in true_res.keys():
            print(sheet)
            self.assertTrue(true_res[sheet].equals(res[sheet]))

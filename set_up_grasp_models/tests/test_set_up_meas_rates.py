import os
import unittest
import pandas as pd

from set_up_grasp_models.set_up_models.set_up_meas_rates import _get_meas_fluxes, _set_up_meas_rates


class TestSetUpMeasRates(unittest.TestCase):

    def setUp(self):
        this_dir, this_filename = os.path.split(__file__)
        self.test_folder = os.path.join(this_dir, 'test_files', 'test_set_up_models', 'set_up_meas_rates')
        self.file_in_meas_fluxes = os.path.join(self.test_folder, 'flux_file_rows.xlsx')
        self.base_df = pd.read_excel(os.path.join(self.test_folder, 'model_v4_manual_fixed.xlsx'), sheet_name=None, index_col=0)

    def test_get_meas_fluxes_rows(self):
        true_res = pd.read_pickle(os.path.join(self.test_folder, 'true_res_rxn_fluxes.pkl'))

        rxns_order = ['R_r1', 'R_r2', 'R_r3', 'R_r4', 'R_r5', 'R_r6', 'R_r7', 'R_r8', 'R_r9', 'R_r10', 'R_r11', 'R_r12',
                      'R_r13', 'R_r14', 'R_r15', 'R_r16', 'R_r17', 'R_r18', 'R_r19', 'R_r20', 'R_r21', 'R_r22', 'R_r23',
                      'R_r24', 'R_r25', 'R_r26', 'R_r27', 'R_r28', 'R_r29', 'R_r30', 'R_r31', 'R_r32', 'R_r33', 'R_r34',
                      'R_r35', 'R_r36', 'R_r37', 'R_r38', 'R_r39', 'R_r40', 'R_r41', 'R_r42', 'R_r43', 'R_r44', 'R_r45',
                      'R_r46', 'R_r47', 'R_r48', 'R_r49']

        res = _get_meas_fluxes(self.file_in_meas_fluxes, rxns_order, orient='rows')

        self.assertTrue(true_res.equals(res))

    def test_get_meas_fluxes_columns(self):
        true_res = pd.read_pickle(os.path.join(self.test_folder, 'true_res_rxn_fluxes.pkl'))

        rxns_order = ['R_r1', 'R_r2', 'R_r3', 'R_r4', 'R_r5', 'R_r6', 'R_r7', 'R_r8', 'R_r9', 'R_r10', 'R_r11', 'R_r12',
                      'R_r13', 'R_r14', 'R_r15', 'R_r16', 'R_r17', 'R_r18', 'R_r19', 'R_r20', 'R_r21', 'R_r22', 'R_r23',
                      'R_r24', 'R_r25', 'R_r26', 'R_r27', 'R_r28', 'R_r29', 'R_r30', 'R_r31', 'R_r32', 'R_r33', 'R_r34',
                      'R_r35', 'R_r36', 'R_r37', 'R_r38', 'R_r39', 'R_r40', 'R_r41', 'R_r42', 'R_r43', 'R_r44', 'R_r45',
                      'R_r46', 'R_r47', 'R_r48', 'R_r49']

        res = _get_meas_fluxes(os.path.join(self.test_folder, 'flux_file_columns.xlsx'), rxns_order, orient='columns')

        self.assertTrue(true_res.equals(res))

    def test_set_up_meas_rates_error(self):
        rxns_order = ['r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12',
                      'r13', 'r14', 'r15', 'r16', 'r17', 'r18', 'r19', 'r20', 'r21', 'r22', 'r23',
                      'r24', 'r25', 'r26', 'r27', 'r28', 'r29', 'r30', 'r31', 'r32', 'r33', 'r34',
                      'r35', 'r36', 'r37', 'r38', 'r39', 'r40', 'r41', 'r42', 'r43', 'r44', 'r45',
                      'r46', 'r47', 'r48', 'r49']

        rxn_fluxes_df = _get_meas_fluxes(os.path.join(self.test_folder, 'flux_file_columns.xlsx'), rxns_order, orient='columns')

        base_df = pd.read_excel(os.path.join(self.test_folder, 'model_v4_manual.xlsx'), sheet_name=None)

        with self.assertRaises(KeyError) as context:
            _set_up_meas_rates(base_df, rxn_fluxes_df, rxns_order)

        self.assertTrue('The reaction IDs in the reaction fluxes dataframe do not match the reaction IDs in the rxns_order variable.' in str(context.exception))

    def test_set_up_meas_rates(self):
        true_res = pd.read_csv(os.path.join(self.test_folder, 'true_res_set_up_meas_rates.csv'), index_col=0)
        true_res.columns = ['vref_mean (mmol/L/h)', 'vref_std (mmol/L/h)', 'vref_mean2 (mmol/L/h)', 'vref_std2 (mmol/L/h)']

        rxns_order = ['R_r1', 'R_r2', 'R_r3', 'R_r4', 'R_r5', 'R_r6', 'R_r7', 'R_r8', 'R_r9', 'R_r10', 'R_r11', 'R_r12',
                      'R_r13', 'R_r14', 'R_r15', 'R_r16', 'R_r17', 'R_r18', 'R_r19', 'R_r20', 'R_r21', 'R_r22', 'R_r23',
                      'R_r24', 'R_r25', 'R_r26', 'R_r27', 'R_r28', 'R_r29', 'R_r30', 'R_r31', 'R_r32', 'R_r33', 'R_r34',
                      'R_r35', 'R_r36', 'R_r37', 'R_r38', 'R_r39', 'R_r40', 'R_r41', 'R_r42', 'R_r43', 'R_r44', 'R_r45',
                      'R_r46', 'R_r47', 'R_r48', 'R_r49']

        rxn_fluxes_df = _get_meas_fluxes(os.path.join(self.test_folder, 'flux_file_columns.xlsx'), rxns_order,
                                         orient='columns')

        res = _set_up_meas_rates(self.base_df, rxn_fluxes_df, rxns_order)

        self.assertTrue(true_res.equals(res))



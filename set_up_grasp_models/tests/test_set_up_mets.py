import os
import unittest
import pandas as pd

from set_up_grasp_models.set_up_models.set_up_mets import _get_mets_conc, _set_up_thermo_mets, _set_up_mets_data


class TestSetUpMets(unittest.TestCase):

    def setUp(self):
        this_dir, this_filename = os.path.split(__file__)
        self.test_folder = os.path.join(this_dir, 'test_files', 'test_set_up_models', 'set_up_mets')
        self.file_in_met_conc = os.path.join(self.test_folder, 'met_concs.xlsx')
        self.base_df = pd.read_excel(os.path.join(self.test_folder, 'model_v1_manual2_EX.xlsx'), sheet_name=None)

    def test_get_mets_conc(self):
        true_res = pd.read_pickle(os.path.join(self.test_folder, 'true_res_met_conc.pkl'))

        mets_order = ['m_glc__D_e', 'm_glc__D_p', 'm_atp_c', 'm_glc__D_c', 'm_adp_c', 'm_pi_c', 'm_g6p_c', 'm_glcn_p',
                      'm_glcn_c', 'm_6pgc_c', 'm_2dhglcn_p', 'm_2dhglcn_c', 'm_6p2dhglcn_c', 'm_nadh_c', 'm_nad_c',
                      'm_nadph_c', 'm_nadp_c', 'm_q8_c', 'm_q8h2_c', 'm_6pgl_c', 'm_co2_c', 'm_ru5p__D_c', 'm_r5p_c',
                      'm_xu5p__D_c', 'm_g3p_c', 'm_s7p_c', 'm_e4p_c', 'm_f6p_c', 'm_2ddg6p_c', 'm_pyr_c', 'm_fdp_c',
                      'm_dhap_c', 'm_13dpg_c', 'm_3pg_c', 'm_2pg_c', 'm_pep_c', 'm_h2o2_c', 'm_gthrd_c', 'm_gthox_c',
                      'm_h2o_c', 'm_pyr_e', 'm_pep_e', 'm_h2o2_e', 'm_g6p_e', 'm_6pgc_e', 'm_r5p_e', 'm_xu5p__D_e',
                      'm_g3p_e', 'm_e4p_e', 'm_f6p_e', 'm_3pg_e']

        res = _get_mets_conc(self.file_in_met_conc, mets_order, orient='columns')

        self.assertTrue(true_res.equals(res))
        
    def test_get_mets_conc_met_list(self):
        true_res = pd.read_pickle(os.path.join(self.test_folder, 'true_res_met_conc.pkl'))

        mets_order = ['glc__D_e', 'glc__D_p', 'atp_c', 'glc__D_c', 'adp_c', 'pi_c', 'g6p_c', 'glcn_p',
                      'glcn_c', '6pgc_c', '2dhglcn_p', '2dhglcn_c', '6p2dhglcn_c', 'nadh_c', 'nad_c',
                      'nadph_c', 'nadp_c', 'q8_c', 'q8h2_c', '6pgl_c', 'co2_c', 'ru5p__D_c', 'r5p_c',
                      'xu5p__D_c', 'g3p_c', 's7p_c', 'e4p_c', 'f6p_c', '2ddg6p_c', 'pyr_c', 'fdp_c',
                      'dhap_c', '13dpg_c', '3pg_c', '2pg_c', 'pep_c', 'h2o2_c', 'gthrd_c', 'gthox_c',
                      'h2o_c', 'pyr_e', 'pep_e', 'h2o2_e', 'g6p_e', '6pgc_e', 'r5p_e', 'xu5p__D_e',
                      'g3p_e', 'e4p_e', 'f6p_e', '3pg_e']

        res = _get_mets_conc(self.file_in_met_conc, mets_order, orient='columns')

        self.assertTrue(true_res.equals(res))

    def test_get_mets_conc_rows(self):
        true_res = pd.read_pickle(os.path.join(self.test_folder, 'true_res_met_conc.pkl'))

        mets_order = ['m_glc__D_e', 'm_glc__D_p', 'm_atp_c', 'm_glc__D_c', 'm_adp_c', 'm_pi_c', 'm_g6p_c', 'm_glcn_p',
                      'm_glcn_c', 'm_6pgc_c', 'm_2dhglcn_p', 'm_2dhglcn_c', 'm_6p2dhglcn_c', 'm_nadh_c', 'm_nad_c',
                      'm_nadph_c', 'm_nadp_c', 'm_q8_c', 'm_q8h2_c', 'm_6pgl_c', 'm_co2_c', 'm_ru5p__D_c', 'm_r5p_c',
                      'm_xu5p__D_c', 'm_g3p_c', 'm_s7p_c', 'm_e4p_c', 'm_f6p_c', 'm_2ddg6p_c', 'm_pyr_c', 'm_fdp_c',
                      'm_dhap_c', 'm_13dpg_c', 'm_3pg_c', 'm_2pg_c', 'm_pep_c', 'm_h2o2_c', 'm_gthrd_c', 'm_gthox_c',
                      'm_h2o_c', 'm_pyr_e', 'm_pep_e', 'm_h2o2_e', 'm_g6p_e', 'm_6pgc_e', 'm_r5p_e', 'm_xu5p__D_e',
                      'm_g3p_e', 'm_e4p_e', 'm_f6p_e', 'm_3pg_e']

        res = _get_mets_conc(os.path.join(self.test_folder, 'met_concs_rows.xlsx'), mets_order, orient='rows')

        self.assertTrue(true_res.equals(res))

    def test_set_up_thermo_mets(self):
        true_res = pd.read_pickle(os.path.join(self.test_folder, 'true_res_thermo_mets.pkl'))

        true_measured_mets = ['m_gthrd_c', 'm_nad_c', 'm_pyr_c', 'm_f6p_c', 'm_g3p_c', 'm_g6p_c', 'm_r5p_c',
                              'm_s7p_c', 'm_ru5p__D_c', 'm_dhap_c', 'm_gthox_c', 'm_nadh_c', 'm_6pgc_c',
                              'm_adp_c', 'm_nadp_c', 'm_pep_c', 'm_fdp_c', 'm_atp_c', 'm_nadph_c']

        mets_order = ['m_glc__D_e', 'm_glc__D_p', 'm_atp_c', 'm_glc__D_c', 'm_adp_c', 'm_pi_c', 'm_g6p_c', 'm_glcn_p',
                      'm_glcn_c', 'm_6pgc_c', 'm_2dhglcn_p', 'm_2dhglcn_c', 'm_6p2dhglcn_c', 'm_nadh_c', 'm_nad_c',
                      'm_nadph_c', 'm_nadp_c', 'm_q8_c', 'm_q8h2_c', 'm_6pgl_c', 'm_co2_c', 'm_ru5p__D_c', 'm_r5p_c',
                      'm_xu5p__D_c', 'm_g3p_c', 'm_s7p_c', 'm_e4p_c', 'm_f6p_c', 'm_2ddg6p_c', 'm_pyr_c', 'm_fdp_c',
                      'm_dhap_c', 'm_13dpg_c', 'm_3pg_c', 'm_2pg_c', 'm_pep_c', 'm_h2o2_c', 'm_gthrd_c', 'm_gthox_c',
                      'm_h2o_c', 'm_pyr_e', 'm_pep_e', 'm_h2o2_e', 'm_g6p_e', 'm_6pgc_e', 'm_r5p_e', 'm_xu5p__D_e',
                      'm_g3p_e', 'm_e4p_e', 'm_f6p_e', 'm_3pg_e']

        mets_conc_df = pd.read_pickle(os.path.join(self.test_folder, 'true_res_met_conc.pkl'))
        mets_conc_res, measured_mets_res = _set_up_thermo_mets(self.base_df, mets_order, mets_conc_df)

        self.assertTrue(true_res.equals(mets_conc_res))
        self.assertListEqual(true_measured_mets, list(measured_mets_res))

    def test_set_up_mets_data(self):
        true_res = pd.read_pickle(os.path.join(self.test_folder, 'true_res_mets_data.pkl'))

        mets_order = ['m_glc__D_e', 'm_glc__D_p', 'm_atp_c', 'm_glc__D_c', 'm_adp_c', 'm_pi_c', 'm_g6p_c', 'm_glcn_p',
                      'm_glcn_c', 'm_6pgc_c', 'm_2dhglcn_p', 'm_2dhglcn_c', 'm_6p2dhglcn_c', 'm_nadh_c', 'm_nad_c',
                      'm_nadph_c', 'm_nadp_c', 'm_q8_c', 'm_q8h2_c', 'm_6pgl_c', 'm_co2_c', 'm_ru5p__D_c', 'm_r5p_c',
                      'm_xu5p__D_c', 'm_g3p_c', 'm_s7p_c', 'm_e4p_c', 'm_f6p_c', 'm_2ddg6p_c', 'm_pyr_c', 'm_fdp_c',
                      'm_dhap_c', 'm_13dpg_c', 'm_3pg_c', 'm_2pg_c', 'm_pep_c', 'm_h2o2_c', 'm_gthrd_c', 'm_gthox_c',
                      'm_h2o_c', 'm_pyr_e', 'm_pep_e', 'm_h2o2_e', 'm_g6p_e', 'm_6pgc_e', 'm_r5p_e', 'm_xu5p__D_e',
                      'm_g3p_e', 'm_e4p_e', 'm_f6p_e', 'm_3pg_e']

        mets_conc_df = pd.read_pickle(os.path.join(self.test_folder, 'true_res_met_conc.pkl'))
        res = _set_up_mets_data(self.base_df, mets_order, mets_conc_df)

        self.assertTrue(true_res.equals(res))

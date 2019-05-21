import os
import unittest
from unittest.mock import patch

import pandas as pd

from set_up_grasp_models.set_up_models.set_up_thermo_rxns import convert_rxns_to_kegg, get_dGs, _parse_rxns, \
    _convert_met_ids_to_kegg, _convert_rxn_str_to_kegg_ids


class TestSetUpThermoRxns(unittest.TestCase):

    def setUp(self):
        self.test_folder = os.path.join('test_files', 'test_set_up_models', 'set_up_thermo_rxns',)
        self.file_bigg_kegg_ids = os.path.join(self.test_folder, 'map_bigg_to_kegg_ids.csv')
        self.rxn_list = ['R_GLCtex: m_glc__D_e <-> m_glc__D_p',
                         'R_GLCabcpp: m_glc__D_p + m_atp_c + m_h2o_c <-> m_glc__D_c + m_adp_c + m_pi_c',
                         'R_GLK: m_glc__D_c + m_atp_c <-> m_adp_c + m_g6p_c', 'R_GLCNtex: m_glcn_e <-> m_glcn_p',
                         'R_GLCNt2rpp: m_glcn_p <-> m_glcn_c', 'R_GNK: m_atp_c + m_glcn_c <-> m_adp_c + m_6pgc_c',
                         'R_2DHGLCNtex: m_2dhglcn_e <-> m_2dhglcn_p', 'R_2DHGLCNkt_tpp: m_2dhglcn_p <-> m_2dhglcn_c',
                         'R_2DHGLCK: m_atp_c + m_2dhglcn_c <-> m_adp_c + m_6p2dhglcn_c',
                         'R_PGLCNDH_NAD: m_6p2dhglcn_c + m_nadh_c <-> m_6pgc_c + m_nad_c',
                         'R_PGLCNDH_NADP: m_6p2dhglcn_c + m_nadph_c <-> m_6pgc_c + m_nadp_c',
                         'R_GLCDpp: m_glc__D_p + m_q8_c <-> m_glcn_p + m_q8h2_c',
                         'R_GAD2ktpp: m_glcn_p + m_q8_c <-> m_q8h2_c + m_2dhglcn_p',
                         'R_G6PDH2: m_g6p_c + m_nadp_c <-> m_6pgl_c + m_nadph_c',
                         'R_G6PDH2_NAD: m_g6p_c + m_nad_c <-> m_6pgl_c + m_nadh_c',
                         'R_G6PDH2_NADP: m_g6p_c + m_nadp_c <-> m_6pgl_c + m_nadph_c',
                         'R_PGL: m_6pgl_c + m_h2o_c <-> m_6pgc_c',
                         'R_GND_NAD: m_nad_c + m_6pgc_c <-> m_nadh_c + m_co2_c + m_ru5p__D_c',
                         'R_GND_NADP: m_nadp_c + m_6pgc_c <-> m_nadph_c + m_co2_c + m_ru5p__D_c',
                         'R_RPI: m_ru5p__D_c <-> m_r5p_c', 'R_RPE: m_ru5p__D_c <-> m_xu5p__D_c',
                         'R_TKT1: m_r5p_c + m_xu5p__D_c <-> m_g3p_c + m_s7p_c',
                         'R_TKT2: m_xu5p__D_c + m_e4p_c <-> m_f6p_c + m_g3p_c',
                         'R_TALA: m_g3p_c + m_s7p_c <-> m_e4p_c + m_f6p_c', 'R_EDD: m_6pgc_c <-> m_2ddg6p_c + m_h2o_c',
                         'R_EDA: m_2ddg6p_c <-> m_g3p_c + m_pyr_c', 'R_PGI: m_g6p_c <-> m_f6p_c',
                         'R_FBP: m_fdp_c + m_h2o_c <-> m_pi_c + m_f6p_c', 'R_FBA: m_g3p_c + m_dhap_c <-> m_fdp_c',
                         'R_TPI: m_g3p_c <-> m_dhap_c', 'R_GAPD: m_pi_c + m_nad_c + m_g3p_c <-> m_nadh_c + m_13dpg_c',
                         'R_PGK: m_adp_c + m_13dpg_c <-> m_atp_c + m_3pg_c', 'R_PGM: m_3pg_c <-> m_2pg_c',
                         'R_ENO: m_2pg_c <-> m_pep_c + m_h2o_c', 'R_PYK: m_adp_c + m_pep_c <-> m_atp_c + m_pyr_c',
                         'R_GTHPi: m_h2o2_c + 2 m_gthrd_c <-> m_gthox_c + 2 m_h2o_c',
                         'R_GTHOr: m_gthox_c + m_nadph_c <-> 2 m_gthrd_c + m_nadp_c',
                         'R_AXPr: m_atp_c <-> m_adp_c + m_pi_c', 'R_NADr: m_nad_c <-> m_nadh_c',
                         'R_NADPr: m_nadp_c <-> m_nadph_c', 'R_EX_pyr: m_pyr_c <-> m_pyr_e',
                         'R_EX_pep: m_pep_c <-> m_pep_e', 'R_EX_h2o2: m_h2o2_e <-> m_h2o2_c']
        self.maxDiff = None

    def test_parse_rxns(self):
        true_met_bigg_ids = {'m_q8h2_c', 'm_g6p_c', 'm_f6p_c', 'm_glc__D_e', 'm_g3p_c', 'm_nadh_c', 'm_atp_c',
                             'm_pep_e', 'm_glc__D_c', 'm_6pgl_c', 'm_h2o2_e', 'm_glc__D_p', 'm_glcn_p', 'm_nad_c',
                             'm_2ddg6p_c', 'm_2pg_c', 'm_nadp_c', 'm_pyr_c', 'm_ru5p__D_c', 'm_e4p_c', 'm_3pg_c',
                             'm_h2o_c', 'm_6pgc_c', 'm_2dhglcn_p', 'm_fdp_c', 'm_nadph_c', 'm_co2_c', 'm_glcn_c',
                             'm_dhap_c', 'm_2dhglcn_c', 'm_gthox_c', 'm_q8_c', 'm_r5p_c', 'm_xu5p__D_c', 'm_pep_c',
                             'm_gthrd_c', 'm_pi_c', 'm_s7p_c', 'm_6p2dhglcn_c', 'm_h2o2_c', 'm_adp_c', 'm_pyr_e',
                             'm_13dpg_c', 'm_2dhglcn_e', 'm_glcn_e'}



        met_bigg_ids = _parse_rxns(self.rxn_list)
        self.assertSetEqual(true_met_bigg_ids, met_bigg_ids)

    def test_convert_met_ids_to_kegg(self):
        true_mets_kegg_dic = {'h2o2': ['C00027'], 'h2o': ['C00001'], 'nad': ['C00003'], 'dhap': ['C00111'],
                              'adp': ['C00008'], 'q8': ['C17569'], '6p2dhglcn': ['C01218'], 'glcn': ['C00257'],
                              'gthrd': ['C00051'], 'pep': ['C00074'], 'xu5p__D': ['C00231'], 'q8h2': '',
                              'glc__D': ['C00031'], 'pi': ['C00009'], 's7p': ['C05382'], 'ru5p__D': ['C00199'],
                              'nadh': ['C00004'], '13dpg': ['C00236'], 'pyr': ['C00022'], 'r5p': ['C03736'],
                              'co2': ['C00011'], 'f6p': ['C00085'], '2pg': ['C00631'], '2dhglcn': ['C06473'],
                              'g6p': ['C00092'], 'nadph': ['C00005'], 'fdp': ['C00354'], 'gthox': ['C00127'],
                              '6pgc': ['C00345'], 'e4p': ['C00279'], 'nadp': ['C00006'], 'atp': ['C00002'],
                              'g3p': ['C00118'], '2ddg6p': ['C04442'], '3pg': ['C00197'], '6pgl': ['C01236']}

        true_mets_without_kegg_id = ['q8h2']

        met_bigg_ids = {'m_q8h2_c', 'm_g6p_c', 'm_f6p_c', 'm_glc__D_e', 'm_g3p_c', 'm_nadh_c', 'm_atp_c',
                        'm_pep_e', 'm_glc__D_c', 'm_6pgl_c', 'm_h2o2_e', 'm_glc__D_p', 'm_glcn_p', 'm_nad_c',
                        'm_2ddg6p_c', 'm_2pg_c', 'm_nadp_c', 'm_pyr_c', 'm_ru5p__D_c', 'm_e4p_c', 'm_3pg_c',
                        'm_h2o_c', 'm_6pgc_c', 'm_2dhglcn_p', 'm_fdp_c', 'm_nadph_c', 'm_co2_c', 'm_glcn_c',
                        'm_dhap_c', 'm_2dhglcn_c', 'm_gthox_c', 'm_q8_c', 'm_r5p_c', 'm_xu5p__D_c', 'm_pep_c',
                        'm_gthrd_c', 'm_pi_c', 'm_s7p_c', 'm_6p2dhglcn_c', 'm_h2o2_c', 'm_adp_c', 'm_pyr_e',
                        'm_13dpg_c', 'm_2dhglcn_e', 'm_glcn_e'}

        map_bigg_to_kegg_ids = pd.read_csv(self.file_bigg_kegg_ids, index_col=0)

        with patch('builtins.input', side_effect=['']):
            mets_kegg_dic, mets_without_kegg_id = _convert_met_ids_to_kegg(met_bigg_ids, map_bigg_to_kegg_ids)

        self.assertDictEqual(true_mets_kegg_dic, mets_kegg_dic)
        self.assertListEqual(true_mets_without_kegg_id, mets_without_kegg_id)

    def test_convert_rxn_str_to_kegg_ids(self):
        true_res = {'R_GLCtex': 'C00031 = C00031', 'R_GLCabcpp': 'C00031 + C00002 + C00001 = C00031 + C00008 + C00009',
                    'R_GLK': 'C00031 + C00002 = C00008 + C00092', 'R_GLCNtex': 'C00257 = C00257',
                    'R_GLCNt2rpp': 'C00257 = C00257', 'R_GNK': 'C00002 + C00257 = C00008 + C00345',
                    'R_2DHGLCNtex': 'C06473 = C06473', 'R_2DHGLCNkt_tpp': 'C06473 = C06473',
                    'R_2DHGLCK': 'C00002 + C06473 = C00008 + C01218',
                    'R_PGLCNDH_NAD': 'C01218 + C00004 = C00345 + C00003',
                    'R_PGLCNDH_NADP': 'C01218 + C00005 = C00345 + C00006',
                    'R_G6PDH2': 'C00092 + C00006 = C01236 + C00005',
                    'R_G6PDH2_NAD': 'C00092 + C00003 = C01236 + C00004',
                    'R_G6PDH2_NADP': 'C00092 + C00006 = C01236 + C00005', 'R_PGL': 'C01236 + C00001 = C00345',
                    'R_GND_NAD': 'C00003 + C00345 = C00004 + C00011 + C00199',
                    'R_GND_NADP': 'C00006 + C00345 = C00005 + C00011 + C00199', 'R_RPI': 'C00199 = C03736',
                    'R_RPE': 'C00199 = C00231', 'R_TKT1': 'C03736 + C00231 = C00118 + C05382',
                    'R_TKT2': 'C00231 + C00279 = C00085 + C00118', 'R_TALA': 'C00118 + C05382 = C00279 + C00085',
                    'R_EDD': 'C00345 = C04442 + C00001', 'R_EDA': 'C04442 = C00118 + C00022', 'R_PGI': 'C00092 = C00085',
                    'R_FBP': 'C00354 + C00001 = C00009 + C00085', 'R_FBA': 'C00118 + C00111 = C00354',
                    'R_TPI': 'C00118 = C00111',
                    'R_GAPD': 'C00009 + C00003 + C00118 = C00004 + C00236',
                    'R_PGK': 'C00008 + C00236 = C00002 + C00197',
                    'R_PGM': 'C00197 = C00631', 'R_ENO': 'C00631 = C00074 + C00001',
                    'R_PYK': 'C00008 + C00074 = C00002 + C00022',
                    'R_GTHPi': 'C00027 + 2 C00051 = C00127 + 2 C00001',
                    'R_GTHOr': 'C00127 + C00005 = 2 C00051 + C00006',
                    'R_AXPr': 'C00002 = C00008 + C00009', 'R_NADr': 'C00003 = C00004', 'R_NADPr': 'C00006 = C00005'}

        mets_kegg_dic = {'h2o2': ['C00027'], 'h2o': ['C00001'], 'nad': ['C00003'], 'dhap': ['C00111'],
                         'adp': ['C00008'], 'q8': ['C17569'], '6p2dhglcn': ['C01218'], 'glcn': ['C00257'],
                         'gthrd': ['C00051'], 'pep': ['C00074'], 'xu5p__D': ['C00231'], 'q8h2': '',
                         'glc__D': ['C00031'], 'pi': ['C00009'], 's7p': ['C05382'], 'ru5p__D': ['C00199'],
                         'nadh': ['C00004'], '13dpg': ['C00236'], 'pyr': ['C00022'], 'r5p': ['C03736'],
                         'co2': ['C00011'], 'f6p': ['C00085'], '2pg': ['C00631'], '2dhglcn': ['C06473'],
                         'g6p': ['C00092'], 'nadph': ['C00005'], 'fdp': ['C00354'], 'gthox': ['C00127'],
                         '6pgc': ['C00345'], 'e4p': ['C00279'], 'nadp': ['C00006'], 'atp': ['C00002'],
                         'g3p': ['C00118'], '2ddg6p': ['C04442'], '3pg': ['C00197'], '6pgl': ['C01236']}

        mets_without_kegg_id = ['q8h2']

        rxn_dict = _convert_rxn_str_to_kegg_ids(self.rxn_list, mets_kegg_dic, mets_without_kegg_id)
        print(rxn_dict)
        self.assertDictEqual(true_res, rxn_dict)

    def test_get_convert_rxns_to_kegg(self):
        true_res = {'R_GLCtex': 'C00031 = C00031', 'R_GLCabcpp': 'C00031 + C00002 + C00001 = C00031 + C00008 + C00009',
                    'R_GLK': 'C00031 + C00002 = C00008 + C00092', 'R_GLCNtex': 'C00257 = C00257',
                    'R_GLCNt2rpp': 'C00257 = C00257', 'R_GNK': 'C00002 + C00257 = C00008 + C00345',
                    'R_2DHGLCNtex': 'C06473 = C06473', 'R_2DHGLCNkt_tpp': 'C06473 = C06473',
                    'R_2DHGLCK': 'C00002 + C06473 = C00008 + C01218',
                    'R_PGLCNDH_NAD': 'C01218 + C00004 = C00345 + C00003',
                    'R_PGLCNDH_NADP': 'C01218 + C00005 = C00345 + C00006',
                    'R_G6PDH2': 'C00092 + C00006 = C01236 + C00005', 'R_G6PDH2_NAD': 'C00092 + C00003 = C01236 + C00004',
                    'R_G6PDH2_NADP': 'C00092 + C00006 = C01236 + C00005', 'R_PGL': 'C01236 + C00001 = C00345',
                    'R_GND_NAD': 'C00003 + C00345 = C00004 + C00011 + C00199',
                    'R_GND_NADP': 'C00006 + C00345 = C00005 + C00011 + C00199', 'R_RPI': 'C00199 = C03736',
                    'R_RPE': 'C00199 = C00231', 'R_TKT1': 'C03736 + C00231 = C00118 + C05382',
                    'R_TKT2': 'C00231 + C00279 = C00085 + C00118', 'R_TALA': 'C00118 + C05382 = C00279 + C00085',
                    'R_EDD': 'C00345 = C04442 + C00001', 'R_EDA': 'C04442 = C00118 + C00022', 'R_PGI': 'C00092 = C00085',
                    'R_FBP': 'C00354 + C00001 = C00009 + C00085', 'R_FBA': 'C00118 + C00111 = C00354',
                    'R_TPI': 'C00118 = C00111', 'R_GAPD': 'C00009 + C00003 + C00118 = C00004 + C00236',
                    'R_PGK': 'C00008 + C00236 = C00002 + C00197', 'R_PGM': 'C00197 = C00631',
                    'R_ENO': 'C00631 = C00074 + C00001', 'R_PYK': 'C00008 + C00074 = C00002 + C00022',
                    'R_GTHPi': 'C00027 + 2 C00051 = C00127 + 2 C00001', 'R_GTHOr': 'C00127 + C00005 = 2 C00051 + C00006',
                    'R_AXPr': 'C00002 = C00008 + C00009', 'R_NADr': 'C00003 = C00004', 'R_NADPr': 'C00006 = C00005'}

        map_bigg_to_kegg_ids = pd.read_csv(self.file_bigg_kegg_ids, index_col=0)

        with patch('builtins.input', side_effect=['']):
            rxn_dict = convert_rxns_to_kegg(self.rxn_list, map_bigg_to_kegg_ids)

        self.assertDictEqual(true_res, rxn_dict)

    def test_get_dGs(self):
        true_res = {'R_GLCtex': (0, 0.0), 'R_GLCabcpp': (-26.39, 0.61), 'R_GLK': (-17.26, 0.72), 'R_GLCNtex': (0, 0.0),
                     'R_GLCNt2rpp': (0, 0.0), 'R_GNK': (-10.11, 3.3), 'R_2DHGLCNtex': (0, 0.0), 'R_2DHGLCNkt_tpp': (0, 0.0),
                     'R_2DHGLCK': (-7.57, 7.8), 'R_PGLCNDH_NAD': (-20.79, 7.25), 'R_PGLCNDH_NADP': (-21.78, 7.26),
                     'R_G6PDH2': (-2.32, 2.12), 'R_G6PDH2_NAD': (-3.31, 2.14), 'R_G6PDH2_NADP': (-2.32, 2.12),
                     'R_PGL': (-20.93, 2.63), 'R_GND_NAD': (10.18, 7.6), 'R_GND_NADP': (11.17, 7.61), 'R_RPI': (-3.63, 7.2),
                     'R_RPE': (-3.37, 1.16), 'R_TKT1': (-2.1, 7.43), 'R_TKT2': (-9.99, 2.09), 'R_TALA': (-0.73, 1.62),
                     'R_EDD': (-43.07, 2.74), 'R_EDA': (15.53, 2.23), 'R_PGI': (2.53, 0.6), 'R_FBP': (-11.43, 0.82),
                     'R_FBA': (-19.8, 0.87), 'R_TPI': (-5.48, 0.75), 'R_GAPD': (7.78, 0.9), 'R_PGK': (-18.45, 0.89),
                     'R_PGM': (4.22, 0.66), 'R_ENO': (-4.08, 0.73), 'R_PYK': (-27.68, 0.94), 'R_GTHPi': (-310.06, 8.05),
                     'R_GTHOr': (-17.42, 1.98), 'R_AXPr': (-184.02, 1.48), 'R_NADr': (64.14, 0.97), 'R_NADPr': (65.13, 0.99)}

        with patch('builtins.input', side_effect=['']):
            rxn_dG_dict = get_dGs(self.rxn_list, self.file_bigg_kegg_ids, pH=7.0, ionic_strength=0.1, digits=2)

        self.assertDictEqual(true_res, rxn_dG_dict)

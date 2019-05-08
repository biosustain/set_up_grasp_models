import os
import unittest

from src.set_up_grasp_models.io.plaintext import import_model_from_plaintext, write_to_plaintext
from src.set_up_grasp_models.io.stoic import import_stoic

TRUE_RXN_LIST = ['ABC: glc_D_p + atp + h2o <-> glc_D + adp + h + p',
                 'GLK: glc_D + atp <-> adp + h + g6p',
                 'ZWF: g6p + nadp <-> h + o_6pgl + nadph',
                 'PGL: o_6pgl + h2o <-> h + o_6pgc',
                 'GNTP: glcn_p + h_p <-> h + glcn',
                 'GNUK: atp + glcn <-> adp + h + o_6pgc',
                 'GCD: glc_D_p + h2o_p + q8_c <-> glcn_p + h_p + q8h2_c',
                 'GAD: glcn_p + fad <-> fadh2 + o_2dhglcn_p',
                 'KGUT: h_p + o_2dhglcn_p <-> h + o_2dhglcn',
                 'KGUK: atp + o_2dhglcn <-> adp + h + o_6p2dhglcn',
                 'KGUD: h + o_6p2dhglcn + nadh <-> o_6pgc + nad',
                 'EDD: o_6pgc <-> h2o + o_2ddg6p',
                 'EDA: o_2ddg6p <-> g3p + pyr',
                 'PGI: f6p <-> g6p',
                 'FBP: h2o + fdp <-> p + f6p',
                 'FBA: g3p + glyc3p <-> fdp',
                 'TPIA: g3p <-> glyc3p',
                 'GAP: p + nad + g3p <-> h + nadh + o_13dpg',
                 'PGK: adp + o_13dpg <-> atp + o_3pg',
                 'GPML: o_3pg <-> o_2pg',
                 'ENO: o_2pg <-> h2o + pep',
                 'PYK: adp + h + pep <-> atp + pyr',
                 'OPRB: glc_D_ex <-> glc_D_p',
                 'PYR_EX: pyr <-> pyr_ex',
                 'GND: nadp + o_6pgc <-> h + nadph + co2 + ru5p_D',
                 'O_3PG_EX: o_3pg <-> o_3pg_ex',
                 'PEP_EX: pep <-> pep_ex',
                 'G6P_EX: g6p <-> g6p_ex',
                 'F6P_EX: f6p_ex <-> f6p',
                 'G3P_EX: g3p <-> 1.5 g3p_ex']


class TestIO(unittest.TestCase):

    def setUp(self):
        self.test_folder = os.path.join('test_files', 'test_io')
        self.file_in_excel = os.path.join(self.test_folder, 'putida_with_PPP.xlsx')
        self.file_in_plaintext = os.path.join(self.test_folder, 'putida_with_PPP_plaintext.txt')

    def test_import_stoic(self):
        mets, rxns, rxn_strings = import_stoic(self.file_in_excel)
        self.assertListEqual(TRUE_RXN_LIST, rxn_strings)

    def test_import_model_from_plaintext(self):
        model = import_model_from_plaintext(self.file_in_plaintext)
        self.assertListEqual(TRUE_RXN_LIST, model.to_string().split('\n'))

    def test_write_to_plaintext(self):
        file_out = os.path.join(self.test_folder, 'plaintext.txt')
        write_to_plaintext(TRUE_RXN_LIST, file_out, print_instructions=True)

        model = import_model_from_plaintext(self.file_in_plaintext)
        self.assertListEqual(TRUE_RXN_LIST, model.to_string().split('\n'))

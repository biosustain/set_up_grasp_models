import unittest
import unittest.mock
import io
import pandas as pd
from src.io.stoic import import_stoic
from src.check_models.format_checks import check_kinetics_met_separators, check_met_rxn_order


class TestFormatChecks(unittest.TestCase):

    def setUp(self):
        self.test_folder = 'test_files/test_check_models'

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_check_kinetics_met_separators_correct(self, mock_stdout):

        true_res = ('\nChecking if values are separated by a space in the kinetics sheet in columns order, ' +
                    'promiscuous, inhibitors, activators, negative effector, and positive effector.\nIt looks for ' +
                    'dots, commas, and semi-colons.\n\n')

        data_dict = pd.read_excel(f'{self.test_folder}/HMP2360_r0_t0.xlsx', sheet_name=None)
        flag = check_kinetics_met_separators(data_dict)

        self.assertEqual(False, flag)
        self.assertEqual(true_res, mock_stdout.getvalue())

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_check_kinetics_met_separators_not_correct(self, mock_stdout):

        true_res = ('\nChecking if values are separated by a space in the kinetics sheet in columns order, ' +
                    'promiscuous, inhibitors, activators, negative effector, and positive effector.\nIt looks for ' +
                    'dots, commas, and semi-colons.\n\n' +
                    'Make sure all metabolites are separated by a single space in column "order" row:\n' +
                    ' pterin1_c trp_c, trp_c fivehtp_c pterin2_c\n\n' +
                    'Make sure all metabolites are separated by a single space in column "order" row:\n' +
                    ' sam_c nactsertn_c meltn_c.sah_c\n\n' +
                    'Make sure all metabolites are separated by a single space in column "order" row:\n' +
                    ' accoa_c srtn_c accoa_c tryptm_c meltn_c;nactsertn_c nactryptm_c coa_c coa_c\n\n' +
                    'Make sure all metabolites are separated by a single space in column "promiscuous" row:\n' +
                    ' AANAT;AANAT_tryptm\n\n')

        data_dict = pd.read_excel(f'{self.test_folder}/HMP2360_r0_t0_not_correct.xlsx', sheet_name=None)
        flag = check_kinetics_met_separators(data_dict)

        self.assertEqual(True, flag)
        self.assertEqual(true_res, mock_stdout.getvalue())

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_check_check_met_rxn_order_correct(self, mock_stdout):

        true_res = '\nChecking if the order of reactions and metabolites is the same in all excel sheets.\n\n'

        data_dict = pd.read_excel(f'{self.test_folder}/HMP2360_r0_t0.xlsx', sheet_name=None)
        flag = check_met_rxn_order(data_dict)

        self.assertEqual(False, flag)
        self.assertEqual(true_res, mock_stdout.getvalue())\


    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_check_check_met_rxn_order_not_correct(self, mock_stdout):

        true_res = ('\nChecking if the order of reactions and metabolites is the same in all excel sheets.\n\n'+
                    'Reaction list in sheet rxns doesn\'t match the list in the stoichiometry matrix.\n' +
                    'Current list:\n' +
                    ' [\'TPH\' \'DDC\' \'AANAT\' \'ASMT\' \'AANAT_tryptm\' \'IN_trp\' \'EX_trp\' \'EX_srtn\'\n' +
                    ' \'EX_fivehtp\' \'EX_nactsertn\' \'EX_meltn\' \'EX_nactryptm\' \'DDC_tryptm\']\n' +
                    'Reaction list in stoichiometric matrix:\n' +
                    ' [\'TPH\' \'DDC\' \'AANAT\' \'ASMT\' \'DDC_tryptm\' \'AANAT_tryptm\' \'IN_trp\' \'EX_trp\'\n' +
                    ' \'EX_srtn\' \'EX_fivehtp\' \'EX_nactsertn\' \'EX_meltn\' \'EX_nactryptm\']\n\n' +
                    'Metabolite list in sheet thermoMets doesn\'t match the list in the stoichiometry matrix.\n' +
                    'Current list:\n' +
                    ' [\'accoa_c\' \'sam_c\' \'pterin1_c\' \'trp_v\' \'fivehtp_c\' \'trp_c\' \'nactsertn_c\'\n' +
                    ' \'meltn_c\' \'tryptm_c\' \'nactryptm_c\' \'coa_c\' \'sah_c\' \'pterin2_c\'\n' +
                    ' \'fivehtp_e\' \'trp_e\' \'nactsertn_e\' \'nactryptm_e\' \'meltn_e\' \'srtn_e\'\n' +
                    ' \'srtn_c\']\n' +
                    'Metabolite list in stoichiometric matrix:\n' +
                    ' [\'accoa_c\' \'sam_c\' \'pterin1_c\' \'trp_v\' \'fivehtp_c\' \'trp_c\' \'srtn_c\'\n' +
                    ' \'nactsertn_c\' \'meltn_c\' \'tryptm_c\' \'nactryptm_c\' \'coa_c\' \'sah_c\'\n' +
                    ' \'pterin2_c\' \'fivehtp_e\' \'trp_e\' \'nactsertn_e\' \'nactryptm_e\' \'meltn_e\'\n' +
                    ' \'srtn_e\']\n\n')

        data_dict = pd.read_excel(f'{self.test_folder}/HMP2360_r0_t0_not_correct.xlsx', sheet_name=None)
        flag = check_met_rxn_order(data_dict)

        self.assertEqual(True, flag)
        self.assertEqual(true_res, mock_stdout.getvalue())

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_check_check_met_rxn_order_not_correct_meas_rates(self, mock_stdout):

        true_res = ('\nChecking if the order of reactions and metabolites is the same in all excel sheets.\n\n'+
                    'Reaction list in sheet rxns doesn\'t match the list in the stoichiometry matrix.\n' +
                    'Current list:\n' +
                    ' [\'TPH\' \'DDC\' \'AANAT\' \'ASMT\' \'AANAT_tryptm\' \'IN_trp\' \'EX_trp\' \'EX_srtn\'\n' +
                    ' \'EX_fivehtp\' \'EX_nactsertn\' \'EX_meltn\' \'EX_nactryptm\' \'DDC_tryptm\']\n' +
                    'Reaction list in stoichiometric matrix:\n' +
                    ' [\'TPH\' \'DDC\' \'AANAT\' \'ASMT\' \'DDC_tryptm\' \'AANAT_tryptm\' \'IN_trp\' \'EX_trp\'\n' +
                    ' \'EX_srtn\' \'EX_fivehtp\' \'EX_nactsertn\' \'EX_meltn\' \'EX_nactryptm\']\n\n' +
                    'Metabolite list in sheet thermoMets doesn\'t match the list in the stoichiometry matrix.\n' +
                    'Current list:\n' +
                    ' [\'accoa_c\' \'sam_c\' \'pterin1_c\' \'trp_v\' \'fivehtp_c\' \'trp_c\' \'nactsertn_c\'\n' +
                    ' \'meltn_c\' \'tryptm_c\' \'nactryptm_c\' \'coa_c\' \'sah_c\' \'pterin2_c\'\n' +
                    ' \'fivehtp_e\' \'trp_e\' \'nactsertn_e\' \'nactryptm_e\' \'meltn_e\' \'srtn_e\'\n' +
                    ' \'srtn_c\']\n' +
                    'Metabolite list in stoichiometric matrix:\n' +
                    ' [\'accoa_c\' \'sam_c\' \'pterin1_c\' \'trp_v\' \'fivehtp_c\' \'trp_c\' \'srtn_c\'\n' +
                    ' \'nactsertn_c\' \'meltn_c\' \'tryptm_c\' \'nactryptm_c\' \'coa_c\' \'sah_c\'\n' +
                    ' \'pterin2_c\' \'fivehtp_e\' \'trp_e\' \'nactsertn_e\' \'nactryptm_e\' \'meltn_e\'\n' +
                    ' \'srtn_e\']\n\n'
                    'Reaction list in sheet measRates doesn\'t match the list in the stoichiometry matrix.\n' +
                    'Current list:\n' +
                    ' [\'TPH\' \'DDC\' \'AANAT\' \'AANAT_tryptm\' \'IN_trp\' \'EX_trp\' \'EX_srtn\'\n' +
                    ' \'EX_fivehtp\' \'EX_nactsertn\' \'EX_meltn\' \'EX_nactryptm\' \'DDC_tryptm\' \'ASMT\']\n' +
                    'Reaction list in stoichiometric matrix:\n' +
                    ' [\'TPH\' \'DDC\' \'AANAT\' \'ASMT\' \'DDC_tryptm\' \'AANAT_tryptm\' \'IN_trp\' \'EX_trp\'\n' +
                    ' \'EX_srtn\' \'EX_fivehtp\' \'EX_nactsertn\' \'EX_meltn\' \'EX_nactryptm\']\n\n')

        data_dict = pd.read_excel(f'{self.test_folder}/HMP2360_r0_t0_not_correct_meas_rates.xlsx', sheet_name=None)
        flag = check_met_rxn_order(data_dict)

        self.assertEqual(True, flag)
        self.assertEqual(true_res, mock_stdout.getvalue())


class TestMassBalanceChecks(unittest.TestCase):

    def setUp(self):
        self.test_folder = 'test_files/test_io'
        self.file_in_excel = f'{self.test_folder}/putida_with_PPP.xlsx'
        self.file_in_plaintext = f'{self.test_folder}/putida_with_PPP_plaintext.txt'

    def test_import_stoic(self):

        mets, rxns, rxn_strings = import_stoic(self.file_in_excel)
        self.assertListEqual(rxn_strings, 1)


class TestThermodynamicsChecks(unittest.TestCase):

    def setUp(self):
        self.test_folder = 'test_files/test_io'
        self.file_in_excel = f'{self.test_folder}/putida_with_PPP.xlsx'
        self.file_in_plaintext = f'{self.test_folder}/putida_with_PPP_plaintext.txt'

    def test_import_stoic(self):

        mets, rxns, rxn_strings = import_stoic(self.file_in_excel)
        self.assertListEqual(rxn_strings, 1)
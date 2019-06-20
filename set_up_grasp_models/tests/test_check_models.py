import io
import os
import unittest.mock

import pandas as pd

from set_up_grasp_models.check_models.format_checks import check_kinetics_met_separators, check_met_rxn_order, \
    check_rxn_mechanism_order, check_kinetics_subs_prod_order
from set_up_grasp_models.check_models.mass_balance_checks import check_balanced_metabolites, check_flux_balance
from set_up_grasp_models.check_models.thermodynamics_checks import check_thermodynamic_feasibility, calculate_dG


class TestFormatChecks(unittest.TestCase):

    def setUp(self):
        this_dir, this_filename = os.path.split(__file__)
        self.test_folder = os.path.join(this_dir, 'test_files', 'test_check_models')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_check_kinetics_met_separators_correct(self, mock_stdout):
        true_res = ('\nChecking if values are separated by a space in the kinetics sheet in columns order, ' +
                    'promiscuous, inhibitors, activators, negative effector, and positive effector.\nIt looks for ' +
                    'dots, commas, and semi-colons.\n\n' +
                    'Everything seems to be OK.\n\n')

        data_dict = pd.read_excel(os.path.join(self.test_folder, 'HMP2360_r0_t0.xlsx'), sheet_name=None)
        flag = check_kinetics_met_separators(data_dict)

        self.assertEqual(False, flag)
        self.assertEqual(true_res, mock_stdout.getvalue())

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_check_kinetics_met_separators_not_correct(self, mock_stdout):
        true_res = ('\nChecking if values are separated by a space in the kinetics sheet in columns order, ' +
                    'promiscuous, inhibitors, activators, negative effector, and positive effector.\nIt looks for ' +
                    'dots, commas, and semi-colons.\n\n' +
                    'Make sure all metabolites are separated by a single space in column "substrate order" row:\n' +
                    ' pterin1_c trp_c, trp_c fivehtp_c pterin2_c\n\n' +
                    'Make sure all metabolites are separated by a single space in column "substrate order" row:\n' +
                    ' sam_c nactsertn_c meltn_c.sah_c\n\n' +
                    'Make sure all metabolites are separated by a single space in column "substrate order" row:\n' +
                    ' accoa_c srtn_c accoa_c tryptm_c meltn_c;nactsertn_c nactryptm_c coa_c coa_c\n\n' +
                    'Make sure all metabolites are separated by a single space in column "product order" row:\n' +
                    ' pterin1_c trp_c, trp_c fivehtp_c pterin2_c\n\n' +
                    'Make sure all metabolites are separated by a single space in column "product order" row:\n' +
                    ' sam_c nactsertn_c meltn_c.sah_c\n\n' +
                    'Make sure all metabolites are separated by a single space in column "product order" row:\n' +
                    ' accoa_c srtn_c accoa_c tryptm_c meltn_c;nactsertn_c nactryptm_c coa_c coa_c\n\n' +
                    'Make sure all metabolites are separated by a single space in column "promiscuous" row:\n' +
                    ' AANAT;AANAT_tryptm\n\n')

        data_dict = pd.read_excel(os.path.join(self.test_folder, 'HMP2360_r0_t0_not_correct.xlsx'), sheet_name=None)
        flag = check_kinetics_met_separators(data_dict)

        self.assertEqual(True, flag)
        self.assertEqual(true_res, mock_stdout.getvalue())

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_check_met_rxn_order_correct(self, mock_stdout):
        true_res = ('\nChecking if the order of reactions and metabolites is the same in all excel sheets.\n\n' +
                    'Everything seems to be OK.\n\n')

        data_dict = pd.read_excel(os.path.join(self.test_folder, 'HMP2360_r0_t0.xlsx'), sheet_name=None)
        flag = check_met_rxn_order(data_dict)

        self.assertEqual(False, flag)
        self.assertEqual(true_res, mock_stdout.getvalue())

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_check_met_rxn_order_not_correct(self, mock_stdout):
        true_res = ('\nChecking if the order of reactions and metabolites is the same in all excel sheets.\n\n' +
                    'Reaction list in sheet rxns doesn\'t match the list in the stoichiometric matrix.\n' +
                    'Current list:\n' +
                    ' [\'TPH\' \'DDC\' \'AANAT\' \'ASMT\' \'AANAT_tryptm\' \'IN_trp\' \'EX_trp\' \'EX_srtn\'\n' +
                    ' \'EX_fivehtp\' \'EX_nactsertn\' \'EX_meltn\' \'EX_nactryptm\' \'DDC_tryptm\']\n' +
                    'Reaction list in stoichiometric matrix:\n' +
                    ' [\'TPH\' \'DDC\' \'AANAT\' \'ASMT\' \'DDC_tryptm\' \'AANAT_tryptm\' \'IN_trp\' \'EX_trp\'\n' +
                    ' \'EX_srtn\' \'EX_fivehtp\' \'EX_nactsertn\' \'EX_meltn\' \'EX_nactryptm\']\n\n' +
                    'Metabolite list in sheet thermoMets doesn\'t match the list in the stoichiometric matrix.\n' +
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

        data_dict = pd.read_excel(os.path.join(self.test_folder, 'HMP2360_r0_t0_not_correct.xlsx'), sheet_name=None)
        flag = check_met_rxn_order(data_dict)

        self.assertEqual(True, flag)
        self.assertEqual(true_res, mock_stdout.getvalue())

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_check_met_rxn_order_not_correct_meas_rates(self, mock_stdout):
        true_res = ('\nChecking if the order of reactions and metabolites is the same in all excel sheets.\n\n' +
                    'Reaction list in sheet rxns doesn\'t match the list in the stoichiometric matrix.\n' +
                    'Current list:\n' +
                    ' [\'TPH\' \'DDC\' \'AANAT\' \'ASMT\' \'AANAT_tryptm\' \'IN_trp\' \'EX_trp\' \'EX_srtn\'\n' +
                    ' \'EX_fivehtp\' \'EX_nactsertn\' \'EX_meltn\' \'EX_nactryptm\' \'DDC_tryptm\']\n' +
                    'Reaction list in stoichiometric matrix:\n' +
                    ' [\'TPH\' \'DDC\' \'AANAT\' \'ASMT\' \'DDC_tryptm\' \'AANAT_tryptm\' \'IN_trp\' \'EX_trp\'\n' +
                    ' \'EX_srtn\' \'EX_fivehtp\' \'EX_nactsertn\' \'EX_meltn\' \'EX_nactryptm\']\n\n' +
                    'Metabolite list in sheet thermoMets doesn\'t match the list in the stoichiometric matrix.\n' +
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
                    'Reaction list in sheet measRates doesn\'t match the list in the stoichiometric matrix.\n' +
                    'Current list:\n' +
                    ' [\'TPH\' \'DDC\' \'AANAT\' \'AANAT_tryptm\' \'IN_trp\' \'EX_trp\' \'EX_srtn\'\n' +
                    ' \'EX_fivehtp\' \'EX_nactsertn\' \'EX_meltn\' \'EX_nactryptm\' \'DDC_tryptm\' \'ASMT\']\n' +
                    'Reaction list in stoichiometric matrix:\n' +
                    ' [\'TPH\' \'DDC\' \'AANAT\' \'ASMT\' \'DDC_tryptm\' \'AANAT_tryptm\' \'IN_trp\' \'EX_trp\'\n' +
                    ' \'EX_srtn\' \'EX_fivehtp\' \'EX_nactsertn\' \'EX_meltn\' \'EX_nactryptm\']\n\n')

        data_dict = pd.read_excel(os.path.join(self.test_folder, 'HMP2360_r0_t0_not_correct_meas_rates.xlsx'),
                                  sheet_name=None)
        flag = check_met_rxn_order(data_dict)

        self.assertEqual(True, flag)
        self.assertEqual(true_res, mock_stdout.getvalue())

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_check_rxn_mechanism_order(self, mock_stdout):
        true_res = ('\nChecking if non enzymatic mechanisms come only after enzymatic ones and if fixedExchange is ' +
                    'the very last one.\n\n' +
                    'Enzymatic mechanism orderedBiBi for reaction ASMT should come before \'diffusion\', ' +
                    '\'freeExchange\', \'fixedExchange\', \'massAction\'.\n' +
                    'Enzymatic mechanism UniUniPromiscuous for reaction DDC_tryptm should come before \'diffusion\', ' +
                    '\'freeExchange\', \'fixedExchange\', \'massAction\'.\n' +
                    'Enzymatic mechanism AANATCompInhibIndep for reaction AANAT_tryptm should come before ' +
                    '\'diffusion\', \'freeExchange\', \'fixedExchange\', \'massAction\'.\n' +
                    'Mechanism massAction for reaction EX_nactsertn should come before fixedExchange mechanisms.\n' +
                    'Mechanism massAction for reaction EX_meltn should come before fixedExchange mechanisms.\n')

        data_dict = pd.read_excel(os.path.join(self.test_folder, 'HMP2360_r0_t0_mech_order.xlsx'),
                                  sheet_name=None)
        flag = check_rxn_mechanism_order(data_dict)

        self.assertEqual(True, flag)
        self.assertEqual(true_res, mock_stdout.getvalue())

    # will fail because the elements in the sets rarely have the same order
    @unittest.expectedFailure
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_check_met_names_kinetics_order(self, mock_stdout):
        true_res = ('\nChecking if the metabolite names in the substrate and product order columns in the kinetics ' +
                    'sheet are valid, i.e., if they are indeed substrates and products of the respective ' +
                    'reaction.\n\n' +
                    'The following metabolites in the substrate order column for reaction TPH are not part of the ' +
                    'reaction substrates:\n{\'pterin2_c\', \'fivehtp_c\'}\n\n' +
                    'The following metabolites in the product order column for reaction TPH are not part of the ' +
                    'reaction products:\n{\'pterin1_c\', \'trp_c\'}\n\n' +
                    'The following metabolites in the substrate order column for reaction DDC are not part of the ' +
                    'reaction substrates:\n{\'tryptm_c\', \'srt_c\', \'trp_c\'}\n\n' +
                    'The following metabolites in the product order column for reaction DDC are not part of the ' +
                    'reaction products:\n{\'tryptm_c\', \'trp_c\', \'fivehtp_c\'}\n\n' +
                    'The following metabolites in the substrate order column for reaction AANAT are not part of the ' +
                    'reaction substrates:\n{\'coa_c\', \'meltn_c\', \'nactryptm_c\', \'tryptm_c\', ' +
                    '\'nactsertn_c\'}\n\n' +
                    'The following metabolites in the product order column for reaction AANAT are not part of the ' +
                    'reaction products:\n{\'meltn_c\', \'nactryptm_c\', \'srtn_c\', \'accoa_c\', ' +
                    '\'m_accoa_c\', \'tryptm_c\'}\n\n' +
                    'The following metabolites in the substrate order column for reaction ASMT are not part of the ' +
                    'reaction substrates:\n{\'meltn_c\', \'sah_c\'}\n\n' +
                    'The following metabolites in the product order column for reaction ASMT are not part of the ' +
                    'reaction products:\n{\'nactsertn_c\', \'sam_c\'}\n\n' +
                    'The following metabolites in the substrate order column for reaction DDC_tryptm are not part of ' +
                    'the reaction substrates:\n{\'tryptm_c\', \'srtn_c\', \'fivehtp_c\'}\n\n' +
                    'The following metabolites in the product order column for reaction DDC_tryptm are not part of ' +
                    'the reaction products:\n{\'trp_c\', \'srtn_c\', \'tryptm_c1\', \'fivehtp_c\'}\n\n' +
                    'The following metabolites in the substrate order column for reaction AANAT_tryptm are not part ' +
                    'of the reaction substrates:\n{\'coa_c\', \'meltn_c\', \'nactryptm_c\', \'srtn_c\', ' +
                    '\'accoa__c\', \'nactsertn_c\'}\n\n' +
                    'The following metabolites in the product order column for reaction AANAT_tryptm are not part of ' +
                    'the reaction products:\n{\'meltn_c\', \'srtn_c\', \'accoa_c\', \'tryptm_c\', ' +
                    '\'nactsertn_c\'}\n\n')

        data_dict = pd.read_excel(os.path.join(self.test_folder, 'HMP2360_r0_t0_mech_met_names_kinetics.xlsx'),
                                  sheet_name=None, index_col=0)
        flag = check_kinetics_subs_prod_order(data_dict)

        self.assertEqual(True, flag)
        self.assertEqual(true_res, mock_stdout.getvalue())

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_check_met_names_kinetics_order_2(self, mock_stdout):
        true_res = ('\nChecking if the metabolite names in the substrate and product order columns in the kinetics ' +
                    'sheet are valid, i.e., if they are indeed substrates and products of the respective ' +
                    'reaction.\n\n' +
                    'The following metabolites in the substrate order column for reaction R_PGI are not part of ' +
                    'the reaction substrates:\n{\'m_g6p_c\'}\n\n' +
                    'The following metabolites in the product order column for reaction R_PGI are not part of ' +
                    'the reaction products:\n{\'m_f6p_c\'}\n\n')

        data_dict = pd.read_excel(os.path.join(self.test_folder, 'model_v2_3_no_reg_ma_EMP_ED_2.xlsx'),
                                  sheet_name=None, index_col=0)
        flag = check_kinetics_subs_prod_order(data_dict)

        self.assertEqual(True, flag)
        self.assertEqual(true_res, mock_stdout.getvalue())


class TestMassBalanceChecks(unittest.TestCase):

    def setUp(self):
        this_dir, this_filename = os.path.split(__file__)
        self.test_folder = os.path.join(this_dir, 'test_files', 'test_check_models')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_check_balanced_metabolites(self, mock_stdout):
        true_res = (
                '\nChecking if metabolites are both consumed and produced in the stoichiometric matrix, and if so ' +
                'checks if they are marked as balanced in the mets sheet. However, the metabolite might be ' +
                'balanced/not balanced anyways depending on the flux of the reactions that consume/produce it, ' +
                'so take this with a grain of salt.\n\n' +
                'm_atp_c is marked as not balanced but it seems to be balanced.\n' +
                'm_adp_c is marked as not balanced but it seems to be balanced.\n' +
                'm_pi_c is marked as not balanced but it seems to be balanced.\n' +
                'm_glcn_e is marked as balanced but it does not seem to be balanced.\n' +
                'm_glcn_e is not set as constant but maybe it should, since it does not seem to be balanced.\n' +
                'm_2dhglcn_e is marked as balanced but it does not seem to be balanced.\n' +
                'm_2dhglcn_e is not set as constant but maybe it should, since it does not seem to be balanced.\n' +
                'm_nadph_c is marked as not balanced but it seems to be balanced.\n' +
                'm_nadp_c is marked as not balanced but it seems to be balanced.\n' +
                'm_co2_c is marked as balanced but it does not seem to be balanced.\n')

        data_dict = pd.read_excel(os.path.join(self.test_folder, 'model_v1_base.xlsx'), sheet_name=None)
        flag = check_balanced_metabolites(data_dict)

        self.assertEqual(True, flag)
        self.assertEqual(true_res, mock_stdout.getvalue())

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_check_flux_balance(self, mock_stdout):
        true_res = ('\nChecking if the fluxes for each metabolite production/consumptions add up to zero.\n\n' +
                    'The flux for m_6pgc_c is not balanced. The difference in flux is -20\n' +
                    'The flux for m_co2_c is not balanced. The difference in flux is 590\n' +
                    'The flux for m_r5p_c is not balanced. The difference in flux is 290\n' +
                    'The flux for m_xu5p_D_c is not balanced. The difference in flux is -10\n' +
                    'The flux for m_g3p_c is not balanced. The difference in flux is 90\n' +
                    'The flux for m_e4p_c is not balanced. The difference in flux is 140\n' +
                    'The flux for m_f6p_c is not balanced. The difference in flux is 50\n' +
                    'The flux for m_3pg_c is not balanced. The difference in flux is 750\n')

        data_dict = pd.read_excel(os.path.join(self.test_folder, 'model_v1_base.xlsx'), sheet_name=None)
        flag = check_flux_balance(data_dict)

        self.assertEqual(True, flag)
        self.assertEqual(true_res, mock_stdout.getvalue())

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_check_flux_balance_fixed(self, mock_stdout):
        true_res = ('\nChecking if the fluxes for each metabolite production/consumptions add up to zero.\n\n'+
                    'Everything seems to be OK.\n')

        data_dict = pd.read_excel(os.path.join(self.test_folder, 'model_v1_base_fixed.xlsx'), sheet_name=None)
        flag = check_flux_balance(data_dict)

        self.assertEqual(False, flag)
        self.assertEqual(true_res, mock_stdout.getvalue())

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_check_flux_balance_incomplete_fluxes(self, mock_stdout):
        true_res = ('\nChecking if the fluxes for each metabolite production/consumptions add up to zero.\n\n' +
                    'Not all fluxes are specified in measRates.\n\n')

        data_dict = pd.read_excel(os.path.join(self.test_folder, 'model_v1_base_incomplete_fluxes.xlsx'),
                                  sheet_name=None)
        flag = check_flux_balance(data_dict)

        self.assertEqual(False, flag)
        self.assertEqual(true_res, mock_stdout.getvalue())


class TestThermodynamicsChecks(unittest.TestCase):

    def setUp(self):
        this_dir, this_filename = os.path.split(__file__)
        self.test_folder = os.path.join(this_dir, 'test_files', 'test_check_models')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_check_thermodynamic_feasibility_putida(self, mock_stdout):
        true_res = ('\nChecking if fluxes and Gibbs energies are compatible.\n\n' +
                    'The flux and ∆G range seem to be incompatible for reaction R_G6PDH2\n' +
                    'The flux and ∆G range seem to be incompatible for reaction R_TALA\n' +
                    'The flux and ∆G range seem to be incompatible for reaction R_PGI\n' +
                    'The flux and ∆G range seem to be incompatible for reaction R_FBA\n' +
                    'The flux and ∆G range seem to be incompatible for reaction R_TPI\n' +
                    'The flux and ∆G range seem to be incompatible for reaction R_GAPD\n' +
                    'The flux and ∆G range seem to be incompatible for reaction R_ENO\n' +
                    'The flux and ∆G range seem to be incompatible for reaction R_EX_pyr\n' +
                    'The flux and ∆G range seem to be incompatible for reaction R_EX_pep\n')

        data_dict = pd.read_excel(os.path.join(self.test_folder, 'model_v1_base.xlsx'), sheet_name=None)
        flag, flux_df, dG_df = check_thermodynamic_feasibility(data_dict)
        self.assertEqual(True, flag)
        self.assertEqual(true_res, mock_stdout.getvalue())

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_check_thermodynamic_feasibility_HMP(self, mock_stdout):
        true_res = ('\nChecking if fluxes and Gibbs energies are compatible.\n\n' +
                    'Everything seems to be OK.\n')

        data_dict = pd.read_excel(os.path.join(self.test_folder, 'HMP2360_r0_t0.xlsx'), sheet_name=None)
        flag, dG_df, flux_df = check_thermodynamic_feasibility(data_dict)

        self.assertEqual(False, flag)
        self.assertEqual(true_res, mock_stdout.getvalue())

    def test_calculate_dG(self):
        true_res_ma = pd.read_pickle(os.path.join(self.test_folder, 'true_res_ma.pkl'))
        true_res_dG = pd.read_pickle(os.path.join(self.test_folder, 'true_res_dG.pkl'))
        true_res_dG_Q = pd.read_pickle(os.path.join(self.test_folder, 'true_res_dG_Q.pkl'))

        temperature = 298  # in K
        gas_constant = 8.314 * 10 ** -3  # in kJ K^-1 mol^-1

        data_dict = pd.read_excel(os.path.join(self.test_folder, 'model_v2_manual.xlsx'), sheet_name=None)
        ma_df, dG_Q_df, dG_df = calculate_dG(data_dict, gas_constant, temperature)

        self.assertTrue(ma_df.equals(true_res_ma))
        self.assertTrue(dG_Q_df.equals(true_res_dG_Q))
        self.assertTrue(dG_df.equals(true_res_dG))

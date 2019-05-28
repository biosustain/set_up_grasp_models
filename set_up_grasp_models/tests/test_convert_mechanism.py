import os
import unittest

import pandas as pd

from set_up_grasp_models.set_up_models.convert_mechanisms import convert_er_mech_to_grasp_pattern, generate_mechanisms


class TestConvertMechanism(unittest.TestCase):

    def setUp(self):
        this_dir, this_filename = os.path.split(__file__)
        self.test_folder = os.path.join(this_dir, 'test_files', 'test_set_up_models', 'convert_mechanism')

    def test_convert_er_mech_to_grasp_pattern_G6PD(self):
        true_res_file = os.path.join(self.test_folder, 'true_res_G6PDH_mech_grasp.txt')

        file_in = os.path.join(self.test_folder, 'G6PDH_mech_er.txt')
        file_out = os.path.join(self.test_folder, 'G6PDH_mech_grasp.txt')

        convert_er_mech_to_grasp_pattern(file_in, file_out, promiscuous=True)

        with open(true_res_file, 'r') as f_in:
            true_res = f_in.read()

        with open(file_out, 'r') as f_in:
            res = f_in.read()

        self.assertEqual(true_res, res)

    def test_convert_er_mech_to_grasp_pattern_AANATCompInhibIndep(self):
        true_res_file = os.path.join(self.test_folder, 'true_res_AANATCompInhibIndep.txt')

        file_in = os.path.join(self.test_folder, 'AANATCompInhibIndep_mech_er.txt')
        file_out = os.path.join(self.test_folder, 'AANATCompInhibIndep_mech_grasp.txt')
        inhib_list = ['mltn_c']

        convert_er_mech_to_grasp_pattern(file_in, file_out, promiscuous=True, inhib_list=inhib_list)

        with open(true_res_file, 'r') as f_in:
            true_res = f_in.read()

        with open(file_out, 'r') as f_in:
            res = f_in.read()

        self.assertEqual(true_res, res)

    def test_convert_er_mech_to_grasp_pattern_G6PDH2CompInhib(self):
        true_res_file = os.path.join(self.test_folder, 'true_res_G6PDH2CompInhib.txt')

        file_in = os.path.join(self.test_folder, 'G6PDH2CompInhib_mech_er.txt')
        file_out = os.path.join(self.test_folder, 'G6PDH2CompInhib_mech_grasp.txt')
        inhib_list = ['m_nadph_c', 'm_nadh_c']

        convert_er_mech_to_grasp_pattern(file_in, file_out, promiscuous=True, inhib_list=inhib_list)

        with open(true_res_file, 'r') as f_in:
            true_res = f_in.read()

        with open(file_out, 'r') as f_in:
            res = f_in.read()

        self.assertEqual(true_res, res)

    def test_convert_er_mech_to_grasp_pattern_orderedBiBi(self):
        true_res_file = os.path.join(self.test_folder, 'true_res_orderedBiBi.txt')

        file_in = os.path.join(self.test_folder, 'orderedBiBi_mech_er.txt')
        file_out = os.path.join(self.test_folder, 'orderedBiBi_mech_grasp.txt')

        convert_er_mech_to_grasp_pattern(file_in, file_out)

        with open(true_res_file, 'r') as f_in:
            true_res = f_in.read()

        with open(file_out, 'r') as f_in:
            res = f_in.read()

        self.assertEqual(true_res, res)

    def test_convert_er_mech_to_grasp_pattern_orderedBiBiActiv(self):
        true_res_file = os.path.join(self.test_folder, 'true_res_orderedBiBiActiv.txt')

        file_in = os.path.join(self.test_folder, 'orderedBiBiActiv_mech_er.txt')
        file_out = os.path.join(self.test_folder, 'orderedBiBiActiv_mech_grasp.txt')
        activ_list = ['pyr_c']

        convert_er_mech_to_grasp_pattern(file_in, file_out, activ_list=activ_list)

        with open(true_res_file, 'r') as f_in:
            true_res = f_in.read()

        with open(file_out, 'r') as f_in:
            res = f_in.read()

        self.assertEqual(true_res, res)

    def test_convert_er_mech_to_grasp_pattern_orderedBiBiActivTwoTracks(self):
        true_res_file = os.path.join(self.test_folder, 'true_res_orderedBiBiActivTwoTracks.txt')

        file_in = os.path.join(self.test_folder, 'orderedBiBiActivTwoTracks_mech_er.txt')
        file_out = os.path.join(self.test_folder, 'orderedBiBiActivTwoTracks_mech_grasp.txt')
        activ_list = ['pyr_c']

        convert_er_mech_to_grasp_pattern(file_in, file_out, activ_list=activ_list)

        with open(true_res_file, 'r') as f_in:
            true_res = f_in.read()

        with open(file_out, 'r') as f_in:
            res = f_in.read()

        self.assertEqual(true_res, res)

    def test_convert_er_mech_to_grasp_pattern_orderedBiBiCompInhib(self):
        true_res_file = os.path.join(self.test_folder, 'true_res_orderedBiBiCompInhib.txt')

        file_in = os.path.join(self.test_folder, 'orderedBiBiCompInhib_mech_er.txt')
        file_out = os.path.join(self.test_folder, 'orderedBiBiCompInhib_mech_grasp.txt')
        inhib_list = ['pyr_c']

        convert_er_mech_to_grasp_pattern(file_in, file_out, inhib_list=inhib_list)

        with open(true_res_file, 'r') as f_in:
            true_res = f_in.read()

        with open(file_out, 'r') as f_in:
            res = f_in.read()

        self.assertEqual(true_res, res)

    def test_convert_er_mech_to_grasp_pattern_orderedBiBiUncompInhib(self):
        true_res_file = os.path.join(self.test_folder, 'true_res_orderedBiBiUncompInhib.txt')

        file_in = os.path.join(self.test_folder, 'orderedBiBiUncompInhib_mech_er.txt')
        file_out = os.path.join(self.test_folder, 'orderedBiBiUncompInhib_mech_grasp.txt')
        inhib_list = ['pyr_c']

        convert_er_mech_to_grasp_pattern(file_in, file_out, inhib_list=inhib_list)

        with open(true_res_file, 'r') as f_in:
            true_res = f_in.read()

        with open(file_out, 'r') as f_in:
            res = f_in.read()

        self.assertEqual(true_res, res)

    def test_convert_er_mech_to_grasp_pattern_orderedBiBiMixedInhib(self):
        true_res_file = os.path.join(self.test_folder, 'true_res_orderedBiBiMixedInhib.txt')

        file_in = os.path.join(self.test_folder, 'orderedBiBiMixedInhib_mech_er.txt')
        file_out = os.path.join(self.test_folder, 'orderedBiBiMixedInhib_mech_grasp.txt')
        inhib_list = ['pyr_c']

        convert_er_mech_to_grasp_pattern(file_in, file_out, inhib_list=inhib_list)

        with open(true_res_file, 'r') as f_in:
            true_res = f_in.read()

        with open(file_out, 'r') as f_in:
            res = f_in.read()

        self.assertEqual(true_res, res)

    def test_convert_er_mech_to_grasp_pattern_orderedBiBiRapidEquilibrium(self):
        true_res_file = os.path.join(self.test_folder, 'true_res_orderedBiBiRapidEquilibrium.txt')

        file_in = os.path.join(self.test_folder, 'orderedBiBiRapidEquilibrium_mech_er.txt')
        file_out = os.path.join(self.test_folder, 'orderedBiBiRapidEquilibrium_mech_grasp.txt')

        convert_er_mech_to_grasp_pattern(file_in, file_out)

        with open(true_res_file, 'r') as f_in:
            true_res = f_in.read()

        with open(file_out, 'r') as f_in:
            res = f_in.read()

        self.assertEqual(true_res, res)

    def test_convert_er_mech_to_grasp_pattern_orderedUniBi(self):
        true_res_file = os.path.join(self.test_folder, 'true_res_orderedUniBi.txt')

        file_in = os.path.join(self.test_folder, 'orderedUniBi_mech_er.txt')
        file_out = os.path.join(self.test_folder, 'orderedUniBi_mech_grasp.txt')

        convert_er_mech_to_grasp_pattern(file_in, file_out)

        with open(true_res_file, 'r') as f_in:
            true_res = f_in.read()

        with open(file_out, 'r') as f_in:
            res = f_in.read()

        self.assertEqual(true_res, res)

    def test_convert_er_mech_to_grasp_pattern_pingPongBiBi(self):
        true_res_file = os.path.join(self.test_folder, 'true_res_pingPongBiBi.txt')

        file_in = os.path.join(self.test_folder, 'pingPongBiBi_mech_er.txt')
        file_out = os.path.join(self.test_folder, 'pingPongBiBi_mech_grasp.txt')

        convert_er_mech_to_grasp_pattern(file_in, file_out)

        with open(true_res_file, 'r') as f_in:
            true_res = f_in.read()

        with open(file_out, 'r') as f_in:
            res = f_in.read()

        self.assertEqual(true_res, res)

    def test_convert_er_mech_to_grasp_pattern_randomBiBi(self):
        true_res_file = os.path.join(self.test_folder, 'true_res_randomBiBi.txt')

        file_in = os.path.join(self.test_folder, 'randomBiBi_mech_er.txt')
        file_out = os.path.join(self.test_folder, 'randomBiBi_mech_grasp.txt')

        convert_er_mech_to_grasp_pattern(file_in, file_out)

        with open(true_res_file, 'r') as f_in:
            true_res = f_in.read()

        with open(file_out, 'r') as f_in:
            res = f_in.read()

        self.assertEqual(true_res, res)

    def test_convert_er_mech_to_grasp_pattern_randomBiBiCompInhib(self):
        true_res_file = os.path.join(self.test_folder, 'true_res_randomBiBiCompInhib.txt')

        file_in = os.path.join(self.test_folder, 'randomBiBiCompInhib_mech_er.txt')
        file_out = os.path.join(self.test_folder, 'randomBiBiCompInhib_mech_grasp.txt')
        inhib_list = ['pyr_c']

        convert_er_mech_to_grasp_pattern(file_in, file_out, inhib_list=inhib_list)

        with open(true_res_file, 'r') as f_in:
            true_res = f_in.read()

        with open(file_out, 'r') as f_in:
            res = f_in.read()

        self.assertEqual(true_res, res)

    def test_convert_er_mech_to_grasp_pattern_randomUniBi(self):
        true_res_file = os.path.join(self.test_folder, 'true_res_randomUniBi.txt')

        file_in = os.path.join(self.test_folder, 'randomUniBi_mech_er.txt')
        file_out = os.path.join(self.test_folder, 'randomUniBi_mech_grasp.txt')

        convert_er_mech_to_grasp_pattern(file_in, file_out)

        with open(true_res_file, 'r') as f_in:
            true_res = f_in.read()

        with open(file_out, 'r') as f_in:
            res = f_in.read()

        self.assertEqual(true_res, res)

    def test_convert_er_mech_to_grasp_pattern_uniUniPromiscuous(self):
        true_res_file = os.path.join(self.test_folder, 'true_res_uniUniPromiscuous.txt')

        file_in = os.path.join(self.test_folder, 'uniUniPromiscuous_mech_er.txt')
        file_out = os.path.join(self.test_folder, 'uniUniPromiscuous_mech_grasp.txt')

        convert_er_mech_to_grasp_pattern(file_in, file_out, promiscuous=True)

        with open(true_res_file, 'r') as f_in:
            true_res = f_in.read()

        with open(file_out, 'r') as f_in:
            res = f_in.read()

        self.assertEqual(true_res, res)

    def test_generate_mechanisms(self):
        hard_coded_mechs = {'massAction', 'diffusion', 'fixedExchange', 'freeExchange'}

        file_in_model = os.path.join(self.test_folder, 'model_v2_manual.xlsx')
        mech_in_dir = os.path.join(self.test_folder, 'mechanisms')
        pattern_out_dir = os.path.join(self.test_folder, 'patterns')

        generate_mechanisms(file_in_model, mech_in_dir, pattern_out_dir)

        model_df = pd.read_excel(file_in_model, sheet_name='kinetics1')
        mech_names = model_df['kinetic mechanism'].values
        mech_names = set(mech_names).difference(hard_coded_mechs)

        for mech in mech_names:
            self.assertTrue(os.path.isfile(os.path.join(pattern_out_dir, mech + '.txt')))

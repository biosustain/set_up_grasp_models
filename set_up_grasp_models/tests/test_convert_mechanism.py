import os
import unittest

from set_up_grasp_models.set_up_models.convert_mechanisms import convert_er_mech_to_grasp_pattern


class TestConvertMechanism(unittest.TestCase):

    def setUp(self):
        self.test_folder = os.path.join('test_files', 'test_set_up_models', 'convert_mechanism')

    def test_convert_er_mech_to_grasp_pattern_G6PD(self):
        true_res_file = os.path.join(self.test_folder, 'true_res_G6PDH_mech_grasp.txt')

        file_in = os.path.join(self.test_folder, 'G6PDH_mech_er.txt')
        file_out = os.path.join(self.test_folder, 'G6PDH_mech_grasp.txt')

        convert_er_mech_to_grasp_pattern(file_in, file_out)

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

        convert_er_mech_to_grasp_pattern(file_in, file_out, inhib_list=inhib_list)

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

        convert_er_mech_to_grasp_pattern(file_in, file_out)

        with open(true_res_file, 'r') as f_in:
            true_res = f_in.read()

        with open(file_out, 'r') as f_in:
            res = f_in.read()

        self.assertEqual(true_res, res)
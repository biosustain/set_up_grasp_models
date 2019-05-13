import os
import unittest

from set_up_grasp_models.set_up_grasp_models.convert_mechanisms import convert_er_mech_to_grasp_pattern


class TestIO(unittest.TestCase):

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

    # TODO add support for inhibitors/activators
    def test_convert_er_mech_to_grasp_pattern_AANATCompInhibIndep(self):
        true_res_file = os.path.join(self.test_folder, 'true_res_AANATCompInhibIndep.txt')

        file_in = os.path.join(self.test_folder, 'AANATCompInhibIndep_mech_er.txt')
        file_out = os.path.join(self.test_folder, 'AANATCompInhibIndep_mech_grasp.txt')

        convert_er_mech_to_grasp_pattern(file_in, file_out)

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

    def test_convert_er_mech_to_grasp_pattern_orderedBiBiCompInhib(self):
        return 0

    def test_convert_er_mech_to_grasp_pattern_orderedBiBiRapidEquilibrium(self):
        return 0

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
        return 0

    def test_convert_er_mech_to_grasp_pattern_randomBiBiCompInhib(self):
        return 0

    def test_convert_er_mech_to_grasp_pattern_randomUniBi(self):
        return 0

    def test_convert_er_mech_to_grasp_pattern_uniUniPromiscuous(self):
        return 0


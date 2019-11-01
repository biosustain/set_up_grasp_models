import os
import unittest

from set_up_grasp_models.set_up_models.set_up_ode_model import convert_to_ode_model


class TestSetUpODEModel(unittest.TestCase):

    def setUp(self):
        self.maxDiff =None
        this_dir, this_filename = os.path.split(__file__)
        self.test_folder = os.path.join(this_dir, 'test_files', 'test_set_up_models', 'set_up_ode_model')
        self.file_in = os.path.join(self.test_folder, 'model_v2_3_all_Kinetics1.m')

    def test_convert_to_ode_model(self):
        true_res_file = os.path.join(self.test_folder, 'true_res_model_v2_3_all_Kinetics1_ode.m')
        with open(true_res_file, 'r') as f_in:
            true_res = f_in.read()

        convert_to_ode_model(self.file_in)

        with open(f'{self.file_in[:-2]}_ode.m', 'r') as f_in:
            res = f_in.read()

        self.assertEqual(true_res, res)


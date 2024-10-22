import unittest
from thinelc import PyPBF
from thinelc.utils import *


class TestPyPBF(unittest.TestCase):

    def setUp(self):
        self.pbf = PyPBF()

    def test_get_string(self):
        self.pbf = PyPBF()
        self.pbf.add_unary_term(0, 0, 1)  # E(x)
        self.pbf.add_unary_term(1, 0, 4)  # 4y
        self.pbf.add_unary_term(2, 0, -1) # -z
        self.pbf.add_pairwise_term(1, 3, 0, 2, 0, 0)  # -2(y-1)w

        vars3 = [0, 1, 2]
        vals3 = [0, 0, 0, 0, 0, 0, 1, 2]  # xy(z+1)
        self.pbf.add_higher_term(3, vars3, vals3)

        vars4 = [0, 1, 2, 3]
        vals4 = [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, -2, 0, -2, 0, -4]  # -xw(y+1)(z+1)
        self.pbf.add_higher_term(4, vars4, vals4)

        self.pbf.shrink()
        str_pbf = self.pbf.get_string()

        str_func = " +1x_{1} +4x_{2} -1x_{3} +2x_{4} -2x_{2}x_{4} +1x_{1}x_{2} -1x_{1}x_{4} +1x_{1}x_{2}x_{3} -1x_{1}x_{3}x_{4} -1x_{1}x_{2}x_{4} -1x_{1}x_{2}x_{3}x_{4} +0"
        self.assertEqual(str_func.strip(), str_pbf.strip())

    def test_parse_input_dict(self):
        self.pbf_tmp = PyPBF()
        input_list = [{0: 1, 1: 4, 2: -1, 3: 2},
                      {(1, 3): -2, (0, 1): 1, (0, 3): -1},
                      {(0, 1, 2): 1, (0, 2, 3): -1, (0, 1, 3): -1},
                      {(0, 1, 2, 3): -1},
                      0]
        self.pbf_tmp = parse_input_dict(self.pbf_tmp, input_list)
        str_pbf = self.pbf_tmp.get_string()
        str_func = " +1x_{1} +4x_{2} -1x_{3} +2x_{4} -2x_{2}x_{4} +1x_{1}x_{2} -1x_{1}x_{4} +1x_{1}x_{2}x_{3} -1x_{1}x_{3}x_{4} -1x_{1}x_{2}x_{4} -1x_{1}x_{2}x_{3}x_{4} +0"
        self.assertEqual(str_func.strip(), str_pbf.strip())

    def test_reduce(self):
        self.pbf_tmp = PyPBF()
        self.qpbf = PyPBF()

        input_list = [{0: 1, 1: 4, 2: -1, 3: 2},
                      {(1, 3): -2, (0, 1): 1, (0, 3): -1},
                      {(0, 1, 2): 1, (0, 2, 3): -1, (0, 1, 3): -1},
                      {(0, 1, 2, 3): -1},
                      0]
        self.pbf_tmp = parse_input_dict(self.pbf_tmp, input_list)
        reduce(self.pbf_tmp, self.qpbf, mode=0, newvar=4)
        str_qpbf = self.qpbf.get_string()
        str_func = " +3x_{1} +4x_{2} -1x_{3} +3x_{4} -4x_{2}x_{4} +2x_{1}x_{2} -4x_{1}x_{4} +1x_{3}x_{4} -2x_{1}x_{3} +0"
        self.assertEqual(str_func.strip(), str_qpbf.strip())

    def test_parse_polynomial(self):
        self.pbf_tmp = PyPBF()
        self.qpbf = PyPBF()
        input_list = [{0: 1, 1: 4, 2: -1, 3: 2},
                      {(1, 3): -2, (0, 1): 1, (0, 3): -1},
                      {(0, 1, 2): 1, (0, 2, 3): -1, (0, 1, 3): -1},
                      {(0, 1, 2, 3): -1},
                      0]
        self.pbf_tmp = parse_input_dict(self.pbf_tmp, input_list)
        reduce(self.pbf_tmp, self.qpbf, mode=0, newvar=4)
        str_qpbf = self.qpbf.get_string()
        output_list = parse_polynomial(str_qpbf, quadratic=True)

        reference_list = [{(0,): 3, (1,): 4, (2,): -1, (3,): 3},
                          {(1, 3): -4, (0, 1): 2, (0, 3): -4, (2, 3): 1, (0, 2): -2}, {0: 0}]
        self.assertEqual(reference_list, output_list)

    def test_e2e_pipeline(self):
        input_list = [{0: 1, 1: 4, 2: -1, 3: 2},
                      {(1, 3): -2, (0, 1): 1, (0, 3): -1},
                      {(0, 1, 2): 1, (0, 2, 3): -1, (0, 1, 3): -1},
                      {(0, 1, 2, 3): -1},
                      0]
        output_list = e2e_pipeline(input_list, mode=0)
        reference_list = [{(0,): 3, (1,): 4, (2,): -1, (3,): 3},
                          {(1, 3): -4, (0, 1): 2, (0, 3): -4, (2, 3): 1, (0, 2): -2}, {0: 0}]
        self.assertEqual(reference_list, output_list)

if __name__ == '__main__':
    unittest.main()
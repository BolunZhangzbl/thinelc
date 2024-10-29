from thinelc import PyPBFInt, PyPBFFloat
from thinelc.utils import *
import os

input_list = [
    # Linear terms
    {4: 13919, 3: 6811, 1: 3349, 0: 4600, 5: 3439, 2: 6122, 7: 5637, 6: 10905, 8: 12125},

    # Quadratic terms
    {(3, 4): -6317, (1, 4): -1452, (1, 3): -167, (0, 4): -1708, (0, 3): -4364, (0, 1): -908,
     (4, 5): -4357, (2, 5): -2993, (2, 4): -1274, (1, 5): -701, (1, 2): -2410, (6, 7): -3840,
     (4, 7): -4469, (4, 6): -2589, (3, 7): -1016, (3, 6): -4098, (7, 8): -5007, (5, 8): -176,
     (5, 7): -61, (4, 8): -1988},

    # Cubic terms
    {(1, 3, 4): -857, (0, 3, 4): 3415, (0, 1, 4): 1392, (0, 1, 3): 1850, (2, 4, 5): 4007,
     (1, 4, 5): -856, (1, 2, 5): 4035, (1, 2, 4): 1712, (4, 6, 7): 3267, (3, 6, 7): 557,
     (3, 4, 7): 3579, (3, 4, 6): 4256, (5, 7, 8): -327, (4, 7, 8): 2461, (4, 5, 8): 1354,
     (4, 5, 7): 1511},

    # Quartic terms
    {(0, 1, 3, 4): -2608, (1, 2, 4, 5): -4259, (3, 4, 6, 7): -4677, (4, 5, 7, 8): -1260},

    # Constant term
    6992
]
# input_list = convert_values(input_list, round_digit=0)


print("test e2e_pipeline: ")
output_list1, num_newvars = e2e_pipeline(input_list, mode=0, use_int=True, display=True)
print(num_newvars)
print("\n")
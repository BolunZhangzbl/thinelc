from thinelc import PyPBFInt, PyPBFFloat
from thinelc.utils import *
import os

abs_path = os.path.abspath(os.path.dirname(__file__))

pbf = PyPBFFloat()
pbf.add_unary_term(0, 0, 1.4554674567256232)  # E(x)
pbf.add_unary_term(1, 0, 4.2234546256562563)  # 4y
pbf.add_unary_term(2, 0, -1.823452654376654) # -z
pbf.add_pairwise_term(1, 3, 0, 2.7523984020333479, 0, 0)  # -2(y-1)w

pbf.shrink()
pbf.print()
print("\n")

vars3 = [0, 1, 2]
vals3 = [0, 0, 0, 0, 0, 0, 1.4523094598751234, 2.0987345612340987]  # xy(z+1)
pbf.add_higher_term(3, vars3, vals3)

pbf.shrink()
pbf.print()
print("\n")

vars4 = [0, 1, 2, 3]
vals4 = [0, 0, 0, 0, 0, 0, 0, 0, 0, -1.0987123456780987, 0, -2.1234567890123456, 0, -2.1234567890123456, 0, -4.1234567890123456]  # -xw(y+1)(z+1)

pbf.add_higher_term(4, vars4, vals4)

print("Higher-order Function: ")
pbf.shrink()
pbf.print()
print("\n")


print("test parse_input_dict: ")
input_list = [{0: 1.455467, 1: 4.223454, 2: -1.823453, 3: 2.752398},
              {(1,3): -2.752398, (0,1): 1.452309, (0,3): -1.098712},
              {(0,1,2): 0.646425, (0,2,3):-1.024744, (0,1,3):-1.024744},
              {(0,1,2,3):-0.975256},
              0.000000]
input_list = convert_values(input_list)
print(input_list)
# save_data(input_list, os.path.join(abs_path, "Q_4_matrix_float.pkl"))

# pbf2 = PyPBFFloat()
# pbf2 = parse_input_dict(pbf2, input_list)
# pbf2.shrink()
# pbf2.print()
#
#
# print(pbf.get_string() == pbf2.get_string())
# print("\n")
#
# qpbf = PyPBFFloat()


print("test e2e_pipeline: \n")
print("mode 0: ")
output_list, num_newvars = e2e_pipeline(input_list, mode=0, use_int=True)
print("\n")

print("mode 1: ")
output_list1, num_newvars1 = e2e_pipeline(input_list, mode=1, use_int=True)
print("\n")

print("mode 2: ")
output_list2, num_newvars2 = e2e_pipeline(input_list, mode=2, use_int=True)
print("\n")
#
# print(output_list == output_list2)
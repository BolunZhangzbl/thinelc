from thinelc import PyPBFInt, PyPBFFloat
from thinelc.utils import *
import os

abs_path = os.path.abspath(os.path.dirname(__file__))

pbf = PyPBFInt()
pbf.add_unary_term(0, 0, 1)  # E(x)
pbf.add_unary_term(1, 0, 4)  # 4y
pbf.add_unary_term(2, 0, -1) # -z
pbf.add_pairwise_term(1, 3, 0, 2, 0, 0)  # -2(y-1)w

pbf.shrink()
pbf.print()
print("\n")

vars3 = [0, 1, 2]
vals3 = [0, 0, 0, 0, 0, 0, 1, 2]  # xy(z+1)
pbf.add_higher_term(3, vars3, vals3)

pbf.shrink()
pbf.print()
print("\n")

vars4 = [0, 1, 2, 3]
vals4 = [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, -2, 0, -2, 0, -4]  # -xw(y+1)(z+1)
pbf.add_higher_term(4, vars4, vals4)

print("Higher-order Function: ")
pbf.shrink()
pbf.print()
print("\n")


print("test parse_input_dict: ")
input_list = [{0: 1, 1: 4, 2: -1, 3: 2},
              {(1,3): -2, (0,1): 1, (0,3): -1},
              {(0,1,2): 1, (0,2,3):-1, (0,1,3):-1},
              {(0,1,2,3):-1},
              0]
save_data(input_list, os.path.join(abs_path, "Q_4_matrix_int.pkl"))
pbf2 = PyPBFInt()
pbf2 = parse_input_dict(pbf2, input_list)
pbf2.shrink()
pbf2.print()


print(pbf.get_string() == pbf2.get_string())
print("\n")

qpbf = PyPBFInt()

# print("test e2e_pipeline: ")
print("mode 0: ")
output_list, num_newvars = e2e_pipeline(input_list, 0)
print(output_list)
print("\n")

print("mode 1: ")
output_list1, num_newvars1 = e2e_pipeline(input_list, 1)
print("\n")

print("mode 2: ")
output_list2, num_newvars2 = e2e_pipeline(input_list, 2)
print(output_list2)
print("\n")


print(output_list == output_list2)
from thinelc import PyPBF
from thinelc.utils import parse_input_dict


pbf = PyPBF()
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
pbf2 = PyPBF()
pbf2 = parse_input_dict(pbf2, input_list)
pbf2.shrink()
pbf2.print()


print(pbf.get_string() == pbf2.get_string())

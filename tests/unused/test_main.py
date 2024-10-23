import re
from thinelc import PyPBFInt

def reduce(pbf, qpbf, mode, newvar):
    assert mode in (0, 1, 2)
    assert isinstance(newvar, int)
    
    if mode==0:
        pbf_tmp = pbf.copy()
        pbf_tmp.reduce_higher()
        pbf_tmp.to_quadratic(qpbf, newvar)
        
    elif mode==1:
        pbf_tmp = pbf.copy()
        pbf_tmp.reduce_higher_approx()
        pbf_tmp.to_quadratic(qpbf, newvar)
    else:
        pbf_tmp = pbf.copy()
        pbf.to_quadratic(qpbf, newvar)
        
        
def convert_numeric_string(num_str):
    # Strip any whitespace from the string
    num_str = num_str.strip()
    # Check if the string represents an integer
    if num_str.isdigit() or (num_str.startswith('-') and num_str[1:].isdigit()):
        return int(num_str)
    # Try to convert to float, will raise ValueError if it fails
    try:
        return float(num_str)
    except ValueError:
        raise ValueError(f"Cannot convert '{num_str}' to a number.")
        
        
def extract_coef_and_vars(input_string):
    # Use a regex to find the coefficient and the variable indices
    match = re.match(r'([-+]?\d*)x_\{([0-9]+)\}?(x_\{([0-9]+)\})?(x_\{([0-9]+)\})?(x_\{([0-9]+)\})?', input_string)

    if not match:
        raise ValueError(f"Input string format is incorrect: {input_string}")

    # Extract the coefficient
    coef_str = match.group(1)

    # Determine the coefficient value
    if coef_str == '' or coef_str == '+':
        coef = 1
    elif coef_str == '-':
        coef = -1
    else:
        coef = int(coef_str)

    # Extract variable indices and subtract 1 to make them 0-indexed
    variables = []
    for i in range(2, 8, 2):  # Match groups for variable indices
        if match.group(i):
            variables.append(int(match.group(i)) - 1)

    # Remove duplicates by converting to a set and then back to a sorted list
    variables = sorted(set(variables))

    # Create a tuple of the variable indices
    tuple_var = tuple(variables)

    return coef, tuple_var
    
        
def parse_polynomial(input_string):
    input_string = input_string.strip()
    list_elems = input_string.split(" ")
    dict_linear = {}
    dict_quadratic = {}
    dict_higher = {}
    dict_constant = {(0): convert_numeric_string(list_elems[-1][1:])}
    
    for elem in list_elems[:-1]:
        coef, tuple_var = extract_coef_and_vars(elem)
        if elem.count('_')==1:
            dict_linear[tuple_var] = coef
        elif elem.count('_')==2:
            dict_quadratic[tuple_var] = coef
        else:
            dict_higher[tuple_var] = coef
                
    return [dict_linear, dict_quadratic, dict_higher, dict_constant]
    


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

print("Higher-order Function (Parsed String): ")
str_pbf = pbf.get_string()
str_pbf_parse = parse_polynomial(str_pbf)
print(str_pbf_parse)
print("\n")


mode = 0
qpbf = PyPBFInt()
reduce(pbf, qpbf, mode, 4)

print("Quadratic Function (mode 0 - ELC+HOCR): ")
qpbf.shrink()
qpbf.print()
print("\n")


print("Quadratic Function (String): ")
str_qpbf = qpbf.get_string()
print(str_qpbf)
print("\n")

print("Quadratic Function (Parsed String): ")
str_qpbf = qpbf.get_string()
str_qpbf_parse = parse_polynomial(str_qpbf)
print(str_qpbf_parse)
print("\n")
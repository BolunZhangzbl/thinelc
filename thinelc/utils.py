# -- Public Imports
import os
import re
import random
import pickle
from itertools import combinations

# -- Private Imports
from thinelc import PyPBFInt, PyPBFFloat

# -- Global Variables


# -- Functions

def generate_random_list(num_vars, max_val, min_val, dtype, max_degree=4, sample=None):
    assert dtype in (int, float)
    result = []

    # Linear terms
    linear_terms = {i: dtype(random.uniform(min_val, max_val)) for i in range(num_vars)}
    result.append(linear_terms)

    # Higher-degree terms up to num_vars
    for degree in range(2, num_vars + 1):
        terms = {}
        indices = list(combinations(range(num_vars), degree))
        for idx in indices:
            terms[idx] = dtype(random.uniform(min_val, max_val))
        result.append(terms)

    # Constant term
    result.append(dtype(random.uniform(min_val, max_val)))

    # Set Max Degree
    result = result[:max_degree] + [result[-1]]

    # Sample certain elements from higher terms
    if sample:
        assert isinstance(sample, int)
        for idx, dict_higher in enumerate(result[1:-1], start=1):
            sampled_keys = random.sample(list(dict_higher.keys()), sample)
            sampled_dict = {key: dict_higher[key] for key in sampled_keys}
            # sampled_dict = dict(list(dict_higher.items())[:sample])
            result[idx] = sampled_dict   # starts from degree 3
    return result


def convert_values(input_list, round_digit=8):
    assert isinstance(round_digit, int)
    assert round_digit <= 8
    for item in input_list:
        if isinstance(item, dict):  # Check if item is a dictionary
            for key in item:
                if isinstance(item[key], float):  # Check if the value is a float
                    # Round to 10 decimal places and then convert to integer
                    if round_digit > 0:
                        item[key] = int(round(item[key], round_digit) * (10 ** round_digit))
                    else:
                        item[key] = float(item[key] * (10 ** round_digit))
    return input_list


def save_data(data, filepath):
    with open(filepath, 'wb') as f:
        pickle.dump(data, f)
    print(f"{os.path.basename(filepath)} has been saved to {filepath}.")


def load_data(filepath):
    with open(filepath, 'rb') as f:
        data = pickle.load(f)
    print(f"{os.path.basename(filepath)} has been loaded from {filepath}.")
    return data


def reduce(pbf, qpbf, mode, newvar):
    assert mode in (0, 1, 2, 3)
    assert isinstance(newvar, int)

    if mode == 0:
        pbf_tmp = pbf
        pbf_tmp.reduce_higher(3)
        pbf_tmp.to_quadratic(qpbf, newvar)
    elif mode == 1:
        pbf_tmp = pbf
        pbf_tmp.reduce_higher_approx()
        pbf_tmp.to_quadratic(qpbf, newvar)
    elif mode == 2:
        pbf_tmp = pbf
        pbf_tmp.to_quadratic(qpbf, newvar)
    else:
        pbf_tmp = pbf
        pbf_tmp.to_quadratic_tin(qpbf, newvar, )


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


def extract_coef_and_vars(input_string, use_int=True):
    # Use a regex to find the coefficient and the variable indices
    if use_int:
        match = re.match(r'([-+]?\d*)x_\{([0-9]+)\}?(x_\{([0-9]+)\})?(x_\{([0-9]+)\})?(x_\{([0-9]+)\})?', input_string)
    else:
        match = re.match(r'([-+]?\d*\.?\d*)x_\{([0-9]+)\}(x_\{([0-9]+)\})?(x_\{([0-9]+)\})?(x_\{([0-9]+)\})?', input_string)

    if not match:
        raise ValueError(f"Input string format is incorrect: {input_string}")

    # Extract the coefficient
    coef_str = match.group(1)

    # Determine the coefficient value
    if coef_str == '' or coef_str == '+':
        coef = 1 if use_int else 1.0
    elif coef_str == '-':
        coef = -1 if use_int else -1.0
    else:
        coef = int(coef_str) if use_int else float(coef_str)

    # Extract variable indices and subtract 1 to make them 0-indexed
    variables = []
    for i in range(2, 8, 2):  # Match groups for variable indices
        if match.group(i):
            variables.append(int(match.group(i)) - 1)

    # Remove duplicates by converting to a set and then back to a sorted list
    # variables = sorted(set(variables))

    # Create a tuple of the variable indices
    tuple_var = tuple(variables)
    tuple_var = tuple_var[0] if len(tuple_var)==1 else tuple_var

    return coef, tuple_var


def parse_polynomial(input_string, quadratic=False, use_int=True):
    input_string = input_string.strip()
    list_elems = input_string.split(" ")
    dict_linear = {}
    dict_quadratic = {}
    dict_higher = {}
    dict_constant = {0: convert_numeric_string(list_elems[-1][1:])}

    for elem in list_elems[:-1]:
        coef, tuple_var = extract_coef_and_vars(elem, use_int=use_int)
        if elem.count('_') == 1:
            dict_linear[tuple_var] = coef
        elif elem.count('_') == 2:
            dict_quadratic[tuple_var] = coef
        else:
            dict_higher[tuple_var] = coef

    list_results = [dict_linear, dict_quadratic, dict_constant] if quadratic else [dict_linear, dict_quadratic, dict_higher, dict_constant]

    return list_results


def parse_input_dict(pbf, input_list):
    assert len(input_list)>=1

    constant_val = input_list[-1]
    for deg, dict_elem in enumerate(input_list[:-1]):
        assert isinstance(dict_elem, dict)
        if deg==0:
            for idx, (key, coef) in enumerate(dict_elem.items()):
                if idx==0:
                    pbf.add_unary_term(key, constant_val, constant_val+coef)
                else:
                    pbf.add_unary_term(key, 0, coef)
        elif deg==1:
            for idx, (key, coef) in enumerate(dict_elem.items()):
                pbf.add_pairwise_term(key[0], key[1], 0, 0, 0, coef)
        else:
            for idx, (key, coef) in enumerate(dict_elem.items()):
                order = deg+1
                vars = list(key)
                vals = [0] * 2**order
                vals[-1] = coef
                pbf.add_higher_term(order, vars, vals)
    return pbf


def random_test(pbf, num_vars, max_val, min_val, sample=20):
    # Linear Terms
    for i in range(num_vars):
        pbf.add_unary_term(i, random.uniform(min_val, max_val), random.uniform(min_val, max_val))

    # Quadratic Term
    for i in range(num_vars-1):
        for j in range(i+1, num_vars):
            pbf.add_pairwise_term(i, j, random.uniform(min_val, max_val), random.uniform(min_val, max_val),
                                  random.uniform(min_val, max_val), random.uniform(min_val, max_val))

    # Higher Term
    for degree in range(3, 5):
        indices = list(combinations(range(num_vars), degree))
        if sample is not None:
            for i in range(sample):
                vars = random.choice(indices)
                vals = [random.randint(min_val, max_val) for _ in range(2**degree)]
                pbf.add_higher_term(degree, vars, vals)
        else:
            for vars in indices:
                vals = [random.randint(min_val, max_val) for _ in range(2 ** degree)]
                pbf.add_higher_term(degree, vars, vals)


def e2e_pipeline(input_list, mode, use_int=True, display=False):

    ### 1. Parse the input list to ELC polynomial
    pbf = PyPBFInt() if use_int else PyPBFFloat()
    pbf = parse_input_dict(pbf, input_list)
    newvar = pbf.max_id() + 1   # the idx of new variables

    if display:
        pbf.shrink()
        pbf.print()
        print("\n")

    ### 2. Perform ELC reduction, pbf -> qpbf
    qpbf = PyPBFInt() if use_int else PyPBFFloat()
    reduce(pbf, qpbf, mode, newvar)

    ### 3. Parse ELC polynomial, qpbf -> output list
    str_qpbf = qpbf.get_string()
    output_list = parse_polynomial(str_qpbf, quadratic=True, use_int=use_int)

    if display:
        qpbf.shrink()
        qpbf.print()
        print("\n")
        print(output_list)
        print("\n")

    num_newvars = qpbf.max_id() - pbf.max_id()

    return output_list, num_newvars




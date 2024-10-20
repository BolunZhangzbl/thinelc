# -- Public Imports


# -- Private Imports


# -- Global Variables


# -- Functions


def reduce(pbf, qpbf, mode, newvar):
    assert mode in (0, 1, 2)
    assert isinstance(newvar, int)

    if mode == 0:
        pbf_tmp = pbf.copy()
        pbf_tmp.reduce_higher()
        pbf_tmp.to_quadratic(qpbf, newvar)

    elif mode == 1:
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
    match = re.match(r'([-+]?\d*)x_\{([0-9]+)\}(x_\{([0-9]+)\})?(x_\{([0-9]+)\})?(x_\{([0-9]+)\})?', input_string)

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

    # Extract variable indices, ignoring None matches
    variables = [
        int(match.group(2)) if match.group(2) else None,
        int(match.group(4)) if match.group(4) else None,
        int(match.group(6)) if match.group(6) else None,
        int(match.group(8)) if match.group(8) else None
    ]

    # Remove None values and create a tuple
    tuple_var = tuple(filter(None, variables))

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
        if elem.count('_') == 1:
            dict_linear[tuple_var] = coef
        elif elem.count('_') == 2:
            dict_quadratic[tuple_var] = coef
        else:
            dict_higher[tuple_var] = coef

    return [dict_linear, dict_quadratic, dict_higher, dict_constant]


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

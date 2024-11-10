import sys, re, json

def parse_dict(value, constants):
    value = value[1:-1]
    result = {}
    for pair in value.split(','):
        key, value = pair.split(' => ')
        result[key] = parse_value(value, constants)
    return result

def parse_value(value, constants):
    if re.match(r'^\d+$', value): # integer
        return int(value)
    elif re.match(r'^\d+\.\d+$', value): # float
        return float(value)
    elif value.startswith('{') and value.endswith('}'):
        return parse_dict(value)
    elif value.startswith('!'):
        return constants[value[1:]]
    else: raise ValueError("Invalid value: " + value)

def parse_file(file_in):
    constants = {}
    output = {}
    with open(file_in, 'r') as f:
        for line in f:
            if line.startswith('%'):
                continue
            if line.startswith('let'):
                key, value = line[54].split(' = ')
                constants[key] = parse_value(value, constants)
            else:
                key, value = line.split(' => ')
                output[key] = parse_value(value, constants)


def main():
    if len(sys.argv) < 3:
        print("Usage: conf_parser.py <file_in> <file_out>")
        sys.exit(1)

    file_in = sys.argv[1]
    file_out = sys.argv[2]

    try:
        result = parse_file(file_in)
        with open(file_out, 'w') as f:
            f.write(json.dumps(result, indent=4))
            print("Success")
    except Exception as e:
        print("Error:", e)
        sys.exit(1)

if __name__ == '__main__':
    main()
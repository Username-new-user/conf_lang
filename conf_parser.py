import sys, re, json

def normalize_lines(lines):
    result = []
    border = 0
    for i, line in enumerate(lines):
        if i < border:
            continue
        if line.endswith('{\n'):
            newlines = []
            bracket_count = 1
            while bracket_count > 0:
                line = line.strip()
                if line.endswith('{'):
                    bracket_count += 1
                if line.startswith('}'):
                    bracket_count -= 1
                newlines.append(line)
                border += 1
                if i + 1 < len(lines):
                    line = lines.pop(i+1)
                    border -= 1
                elif len(lines) == 1:
                    lines = []
            newlines = newlines[0:-1]
            result.append(' '.join(normalize_lines(newlines)))
        else:
            result.append(line)
    return result
        

def get_pairs(value):
    pairs = []
    bracket_count = 0
    start = 0
    for i, c in enumerate(value):
        if c == '{':
            bracket_count += 1
        if c == '}':
            bracket_count -= 1
        if c == ',' and bracket_count == 0:
            pairs.append(value[start:i])
            start = i + 1
    pairs.append(value[start:])
    return pairs

def parse_dict(value, constants):
    value = value[1:-1]
    print(value)
    result = {}
    pairs = get_pairs(value)
    #for pair in value.split(','):
    for pair in pairs:
        print('pair:', pair)
        key = pair.split(' => ')[0].strip()
        value = ' => '.join(pair.split(' => ')[1:])
        if value.endswith(' '):
            value = value[0:-1]
        print('key:', key, 'value:', [value])
        result[key] = parse_value(value, constants)
        print('result:', result)
    return result

def parse_value(value, constants):
    if re.match(r'^\d+$', value): # integer
        return int(value)
    elif re.match(r'^\d+\.\d+$', value): # float
        return float(value)
    elif value.startswith('{') and value.endswith('}'):
        return parse_dict(value, constants)
    elif value.startswith('!'):
        print(constants, value)
        return constants[value[1:]]
    elif value.startswith('\"'):
        return value.replace('\"', '').replace('\n', '')
    else: 
        raise ValueError("Invalid value: " + value)

def parse_file(file_in):
    constants = {}
    output = {}
    with open(file_in, 'r') as f:
        lines = f.readlines()
        border = -1
        lines = normalize_lines(lines)
        print('normalized lines:', lines)
        for i, line in enumerate(lines):
            if line.startswith('%') or i < border:
                continue
            if line.startswith('let'):
                key, value = line[4:].split(' = ')
                constants[key] = parse_value(value, constants)
            elif '{' in line:
                key = line[0:line.find('{')].strip()
                value = parse_value(line[line.find('{'):].strip(), constants)
                output[key] = value
            else:
                key, value = line.split(' => ')
                output[key] = parse_value(value, constants)
    return output


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

# Пример использования
'''
with open('input_db.txt', 'r') as f:
    lines = normalize_lines(f.readlines())
for line in lines:
    print(line)
print(len(lines))
'''
if __name__ == '__main__':
    main()

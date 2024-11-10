import sys, re, json

def parse_dict():
    pass

def parse_string():
    pass

def parse_file():
    pass

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
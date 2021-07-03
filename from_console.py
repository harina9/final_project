import argparse
from initialization import initialize_program

parser = argparse.ArgumentParser(description='Weather_analyzer')
parser.add_argument('data', type=str, help='Input dir')
parser.add_argument('output_dir', type=str, help='Output')
args = parser.parse_args()

if __name__ == '__main__':
    initialize_program(args.data, args.output_dir)
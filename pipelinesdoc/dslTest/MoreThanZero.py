import argparse
import os

def MoreThanZero(data):
    addData = 0
    for line in data:
       addData += int(line)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--data',required=True,help='local file to be input')
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    MoreThanZero(args.data)

if __name__ == '__main__':
    main()
import argparse

def SumNumber(data1,data2,data3):
    sumNumber = 80


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--data1',required=True,help='local file to be input')
    parser.add_argument('--data2',required=True,help='local file to be input')
    parser.add_argument('--data3',required=True,help='local file to be input')
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    SumNumber(args.data1,args.data2,args.data3)

if __name__ == '__main__':
    main()
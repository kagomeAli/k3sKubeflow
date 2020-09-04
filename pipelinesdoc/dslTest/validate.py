import argparse

def validate(data,deliveryNum):
    more = []
    less = []
    for line in lines:
        num = int(line)
        if num > deliveryNum:
            moreData.append(num)
        elif num < deliveryNum:
            lessData.append(num)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument( '--data',type=str,required=True,help='local file to be input')
    parser.add_argument('--deliveryNum',type=str,required=True,help='local file to be input')
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    validate(args.data,args.deliveryNum)

if __name__ == '__main__':
    main()
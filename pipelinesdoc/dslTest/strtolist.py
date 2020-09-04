import argparse
import os

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument( '--output_dir',type=str,required=True,help='local file to be input')
    parser.add_argument('--data',type=str,required=True,help='local file to be input')
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    output_dir = args.output_dir
    print(output_dir)
    strData = args.data

    output_path=os.path.join(output_dir, 'square.txt')
    f1 = open(output_path,'w')
    for line in result:
       sum = int(line) * int(line)
       f1.write(str(sum) + "\n")
    f1.close()

    result = strData.split(',')
    print(result)

if __name__ == '__main__':
    main()
import argparse
import ssEnergy as s
from typing import List

def argParser():
    parser = argparse.ArgumentParser(description="Count hairpins in RNA dotbracket file")
    parser.add_argument("-f", "--file", help="File to process")
    parser.add_argument("-i", "--input", help="Input sequence to process")
    args = parser.parse_args()
    return args

def cntHairpins(sequence: str) -> int:

    s = sequence.strip()
    stack = []
    hairpins = 0

    for i, ch in enumerate(s):
        if ch == '(':
            stack.append(i)
        elif ch == ')':
            j = stack.pop()
            if '(' not in s[j+1:i]:
                hairpins += 1
    return hairpins

def cntFromFile(lines: List[str]) -> List[int]:

    results = []
    for line in lines:
        if line.startswith(("(", ".")):
            struct = line.split()[0]
            results.append(cntHairpins(struct))
    return results

def main():
    args = argParser()
    if args.input:
        print(f"Hairpins count in each sequence: {cntHairpins(args.input)}")
    else:
        file = s.readFile(args.file)
        print(f"Hairpins count in each sequence: {cntFromFile(file)}")


if __name__ == "__main__":
    main()

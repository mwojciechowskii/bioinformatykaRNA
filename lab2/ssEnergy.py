import argparse
import threading
import itertools, sys, time
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple

"""
ZADANIE 2 PUNKT 6
przy zalozeniu faktycznego zliczenia wszystkich pojedynczych nukleotydow,
matplotlib sobie nie radzi z rysowaniem wykresu, a rozwiazanie ponizej z tym pomaga
"""
import matplotlib as mpl
mpl.rcParams['agg.path.chunksize'] = 10000

def animate(stop):
    """
    REF:
    https://stackoverflow.com/questions/22029562/python-how-to-make-simple-animated-loading-while-process-is-running
    """
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if stop.is_set():
            break
        sys.stdout.write('\rGenerating plot  ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\n')

def argParser():
    parser = argparse.ArgumentParser(description="Process RNA dot bracket file")
    parser.add_argument("file", help="File to process")
    args = parser.parse_args()
    return args

def readFile(file: str) -> List[str]:
    with open(file, 'r') as f:
        return f.read().splitlines()

def cntSS(file: List[str]) -> Tuple[List[int], List[float]]:
    
    dots, energyList = [], []
    for line in file:
        if line.startswith(("(", ".")):
            lineDotCnt, energy = line.split(' ', 1)
            dots.append(lineDotCnt.count('.'))
            energyList.append(float(energy))
        else: continue

    return dots, energyList
    
def generatePlot(dotCounts: List[int], energyCounts: List[float]):

    plt.figure(figsize=(8, 5))
    plt.scatter(dotCounts, energyCounts, color="darkgreen", s=10, alpha=0.7, label="energy")
    plt.xlabel("Number of dots (unpaired bases)")
    plt.ylabel("Energy")
    plt.title("Energy vs dot-count")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
    plt.close()

def countCorrCoefficient(dotCounts: List[int], energyCounts: List[float]) -> float:
    
    dcARR = np.array(dotCounts, dtype=float)
    enARR = np.array(energyCounts, dtype=float)
    return np.corrcoef(dcARR, enARR)[0, 1]

def main():

    args = argParser()
    file = readFile(args.file)
    dotCounts, energyCounts = cntSS(file)

    result = countCorrCoefficient(dotCounts, energyCounts)
    print(f"correlation coefficient: {result}")

    stopRun = threading.Event()
    #daemon=True fixes keyboard interruption
    t = threading.Thread(target=animate, args=(stopRun,), daemon=True)
    t.start()

    generatePlot(dotCounts, energyCounts)

    stopRun.set()
    t.join()

    """
    n = sum(key for d in ssCnt for key in d.keys())
    print(n)
    """

if __name__ == "__main__":
    main()

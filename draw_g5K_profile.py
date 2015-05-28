__author__ = 'alebre'

import json
import sys
import matplotlib.pyplot as plt
import numpy as np
def main():
    # Get the input
    result_file_path = './result.json'
    try:
        with open(result_file_path) as publis_file:
            publis = json.load(publis_file)
    except:
        print 'The file %s is not available or does not follows a json structure' % result_file_path
        return

    year_pubs = {y: len(filter(lambda c : c['year'] == y, publis)) for y in range(2009, 2016)}
    x_pos = np.arange(len(year_pubs.keys()))
    print (np.mean(year_pubs.values()))
    plt.bar(x_pos, year_pubs.values(), color='orange', align='center')
    plt.xticks(x_pos, year_pubs.keys())
    plt.title('Nbre de publications par an depuis 2009')
    plt.show()

if __name__ == "__main__":
    sys.exit(main())
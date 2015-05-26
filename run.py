__author__ = 'alebre'

import json
import sys
from lib import filter_G5K_pub, make_scholar_request_from_filtered_json


def main():

    worker_id = 1
    # Get the input
    try:
        with open('./data/index-g5k.json') as data_file:
            data = json.load(data_file)
    except:
        with open('./data/index.json') as data_file:
            data_non_filtered = json.load(data_file)
            data = filter_G5K_pub(data_non_filtered)
            with open('./data/index-g5k.json', 'w') as outfile_g5k:
                json.dump(data, outfile_g5k)

    # Get the input
    result_file_path = './data/result_%i.json' % (worker_id)

    for i in range(0, 30):
        try:
            with open(result_file_path) as parsed_data_file:
                parsed_data = json.load(parsed_data_file)
        except:
            parsed_data = []

        print len(parsed_data)

        result = make_scholar_request_from_filtered_json(data, parsed_data,
                                                         worker_id)

        with open(result_file_path, 'w') as outfile:
            json.dump(result, outfile)


if __name__ == "__main__":
    sys.exit(main())
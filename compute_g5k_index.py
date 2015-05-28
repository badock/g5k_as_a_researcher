__author__ = 'alebre'


import json
import sys
import time

def compute_citations_number(publis):
    citation_nb = 0
    not_evaluated = 0
    h_index = 0
    i_index = 0
    sorted_publis =  sorted(publis, key=lambda publi: publi['citation_count'])
    for publi in sorted_publis:
        if publi['citation_count'] < 0:
            not_evaluated = not_evaluated + 1
        else:
            citation_nb = citation_nb + publi['citation_count']
            if (publi['citation_count'] > h_index):
                h_index = h_index + 1
            if (publi['citation_count'] >= 10):
                i_index = i_index + 1
    print 'g5k profile: citations nb %d, h_index %d, i_index %d (not_evaluated %d)' % (citation_nb, h_index, i_index, not_evaluated)


def get_year(raw_publis, title):
    for raw_publi in raw_publis:
        if raw_publi['title'] == title:
            return raw_publi['submission_date']
    return -1

def add_year (raw_publis, publis):
    result=[]
    for publi in publis:
        line = {'title': publi['title'], 'citation_count': publi['citation_count'], 'year': time.strptime(get_year(raw_publis, publi['title']), "%Y-%m-%d").tm_year}
        print line
        result += [line]
    return result

def main():
    # Get the input
    result_file_path = './result.json'
    try:
        with open(result_file_path) as publis_file:
            publis = json.load(publis_file)
    except:
        print 'The file %s is not available or does not follows a json structure' % result_file_path
        return

    try:
        with open('./index-g5k.json') as data_file:
           data = json.load(data_file)
    except:
        print 'The file %s is not available or does not follows a json structure' % result_file_path
        return

   # publis_year = add_year(data, publis)
    publis_year = publis

    print 'There are %d publications' % len(publis_year)

    compute_citations_number(publis_year)

    with open ('./result.json', 'w') as outfile:
        json.dump(publis_year, outfile)

if __name__ == "__main__":
    sys.exit(main())
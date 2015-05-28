__author__ = 'alebre'

import json
import scholar
import sys
import time
import traceback
from random import randint


def make_scholar_request_fromhal(data, parsed_data):
    result=[]
    for internal_key in data:
        domains = data[internal_key]['domains'] # because there is one internal level, I don't know why but ..
        for domain_key in domains:
            teams = domains[domain_key]['teams']
            for team_key in teams:
                publis = teams[team_key]['publis']
                for publi in publis:
                    #print publi['title']
                    #               cmd = '/TRASH/scholar.py/scholar.py -d --phrase "%s"' % (publi['title'])
                    #               res = os.system(cmd)
                    #               print res
                    if publi['type'] == 'found-in-pdf' or publi['type'] == 'found-in-collaboration':
                        if not is_parsed(publi['title'], parsed_data+result):
                            querier = scholar.ScholarQuerier()
                            query = scholar.SearchScholarQuery()
                            query.set_num_page_results(1)
                            query.set_phrase(publi['title'])
                            # query.set_phrase('Entropy: a consolidation manager for clusters')
                            querier.send_query(query)
                            try:
                                line = {'title': publi['title'], 'citation_count': querier.articles[0]['num_citations']}
                                # print publi['title']:querier.articles[0]['num_citations']
                                print line
                            except:
                                print 'error %s' % (publi['title'])
                                print(traceback.format_exc())
                       #         line = {'title': publi['title'], 'citation_count': 0}

                            result+=[line]
                            if len(result) > 10:
                                return parsed_data+result
                            # just wait before making the new query
                            time.sleep(randint(40,120))

    return parsed_data+result


def make_scholar_request(title):
    citations_nb = 0
    querier = scholar.ScholarQuerier()
    query = scholar.SearchScholarQuery()
    query.set_num_page_results(1)
    query.set_phrase(title)
    if (querier.send_query(query)) == True :
        if(len(querier.articles) >= 1):
            citations_nb = querier.articles[0]['num_citations']
        else:
            citations_nb = -1
    else:
        print 'Error 503'
        citations_nb = -2
    return citations_nb



def get_year(raw_publis, title):
    for raw_publi in raw_publis:
        if raw_publi['title'] == title:
            return raw_publi['submission_date']
    return -1


# worker_id = 0 or 1
def make_scholar_request_from_filtered_json(raw_publis, parsed_data):

    result=[]

    for publi in raw_publis:
        if publi['type'] == 'found-in-pdf' or publi['type'] == 'found-in-collaboration':
            if not is_parsed(publi['title'], parsed_data+result):
                citations_nb = make_scholar_request(publi['title'])
                line = {'title': publi['title'], 'citation_count': citations_nb, 'year': time.strptime(get_year(raw_publis, publi['title']), "%Y-%m-%d").tm_year}
                print line
                result += [line]
                if len(result) > 10:
                    return parsed_data+result

                # just wait before making the new query
                time.sleep(randint(40, 120))

    return parsed_data + result


def is_parsed(title, data):
    for line in data:
        if line['title'] == title:
            return True
    return False


# Retrieve all publications related to G5K (and only related to G5K)
# data, the json file returned by g5kbib
def filter_G5K_pub(data):
    result=[]
    for internal_key in data:
        domains = data[internal_key]['domains'] # because there is one internal level, I don't know why but ..
        for domain_key in domains:
            teams = domains[domain_key]['teams']
            for team_key in teams:
                publis = teams[team_key]['publis']
                for publi in publis:
                    if publi['type'] == 'found-in-pdf' or publi['type'] == 'found-in-collaboration':
                        result += [publi]
                        print publi

    return result


def check_nonevaluated(list_publis):
    for publi in list_publis:
        if(publi['citation_count'] <= -1):
            publi['citation_count']= make_scholar_request(publi['title'])
            # wait before making the next query if the previous one succeeded.
            if (publi['citation_count'] > -2):
                time.sleep(randint(40, 120))

def main():

    # Get the input
    try:
        with open('./index-g5k.json') as data_file:
            data = json.load(data_file)
    except:
        with open('./index.json') as data_file:
            data_non_filtered = json.load(data_file)
            data = filter_G5K_pub(data_non_filtered)
            with open ('./index-g5k.json', 'w') as outfile_g5k:
                json.dump(data, outfile_g5k)

    # Get the input
    result_file_path = './result.json'

    for i in range(0, 30):
        try:
            with open(result_file_path) as parsed_data_file:
                parsed_data = json.load(parsed_data_file)
        except:
            parsed_data=[]

        print len(parsed_data)

        result = make_scholar_request_from_filtered_json(data,parsed_data)

        with open (result_file_path, 'w') as outfile:
            json.dump(result, outfile)

    # Check once again the non evaluated request (request that get either no publication or 503 error)
    check_nonevaluated(result)
    with open (result_file_path, 'w') as outfile:
        json.dump(result, outfile)

if __name__ == "__main__":
    sys.exit(main())

__author__ = 'jonathan'

from scholar import scholar as scholar
import time

from random import randint

# def make_scholar_request_fromhal(data, parsed_data):
#     result=[]
#     for internal_key in data:
#         domains = data[internal_key]['domains'] # because there is one internal level, I don't know why but ..
#         for domain_key in domains:
#             teams = domains[domain_key]['teams']
#             for team_key in teams:
#                 publis = teams[team_key]['publis']
#                 for publi in publis:
#                     #print publi['title']
#                     #               cmd = '/TRASH/scholar/scholar -d --phrase "%s"' % (publi['title'])
#                     #               res = os.system(cmd)
#                     #               print res
#                     if publi['type'] == 'found-in-pdf' or publi['type'] == 'found-in-collaboration':
#                         if not is_parsed(publi['title'], parsed_data+result):
#                             querier = scholar.ScholarQuerier()
#                             query = scholar.SearchScholarQuery()
#                             query.set_num_page_results(1)
#                             query.set_phrase(publi['title'])
#                             # query.set_phrase('Entropy: a consolidation manager for clusters')
#                             querier.send_query(query)
#                             try:
#                                 line = {'title': publi['title'], 'citation_count': querier.articles[0]['num_citations']}
#                                 # print publi['title']:querier.articles[0]['num_citations']
#                                 print line
#                                 result += [line]
#                                 if len(result) > 10:
#                                     return parsed_data+result
#                             except:
#                                 print 'error %s' % (publi['title'])
#                                 print(traceback.format_exc())
#                             # just wait before making the new query
#                             time.sleep(randint(40,120))
#
#     return parsed_data+result

# worker_id = 0 or 1
def make_scholar_request_from_filtered_json(data, parsed_data, worker_id):
    result=[]
    for publi in data:
        index = data.index(publi)
        if (index % 2) != worker_id:
            continue
        if publi['type'] == 'found-in-pdf' or publi['type'] == 'found-in-collaboration':
            # print index
            # continue
            if not is_parsed(publi['title'], parsed_data+result):
                querier = scholar.ScholarQuerier()
                query = scholar.SearchScholarQuery()
                query.set_num_page_results(1)
                query.set_phrase(publi['title'])
                # query.set_phrase('Entropy: a consolidation manager for clusters')
                request_success = querier.send_query(query)
                if request_success:
                    if len(querier.articles) > 0:
                        line = {'title': publi['title'], 'citation_count': querier.articles[0]['num_citations']}
                    else:
                        line = {'title': publi['title'], 'citation_count': -1}
                    print line
                    result += [line]
                    if len(result) > 10:
                        return parsed_data+result
                else:
                    print 'Error 503'
                # just wait before making the new query
                time.sleep(randint(40, 120))
    return parsed_data+result


def is_parsed(title, data):
    for line in data:
        if line['title'] == title:
            return True
    return False

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
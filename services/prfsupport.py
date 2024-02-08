"""
File which supports psuedo relevance feedback decision making
"""

from indexer import es
from configs import INDEX_NAME,PRF_OUT_PATH,models
# from queryProcessors import score_generator,filewriter

def prf_highterm_fetcher(data_combined):

    # top3term_score_dict = {}

    # Flatten the data to get all terms with their scores
    all_terms_with_scores = [(item['key'], item['score']) for sublist in data_combined for item in sublist]

    # Sort the terms by their scores in descending order
    sorted_terms_with_scores = sorted(all_terms_with_scores, key=lambda x: x[1], reverse=True)

    # Extract the top 5 unique terms based on score
    top_5_terms = []
    seen_keys = set()
    for term, score in sorted_terms_with_scores:
        if term not in seen_keys:
            top_5_terms.append((term))
            seen_keys.add(term)
        if len(top_5_terms) == 5:
            break

    return top_5_terms

def relevant_terms_fetch(INDEX_NAME,doc_id):
    document = es.get(index=INDEX_NAME, id=doc_id)
    required_content = document["_source"]["_content"]

    response = es.search(
        index=INDEX_NAME,
        body={
        "query" : {
            "terms" : {
                "_content" : required_content.split(" ")
            }
        },
        "aggregations" : {
            "relatedTerms" : {
                "significant_terms" : {
                    "field" : "_content"
                }
            }

        },
        "size": 0
        }
    )

    outresp = response['aggregations']['relatedTerms']['buckets']

    return outresp


# def prf_driver(queries,query_ids,attributes_dict,query_scores,document_list,limit):
    
#     prf_dict = {}

#     for query_id,doc_scores in query_scores['tfidf'].items():
#         first_five_docs = list(doc_scores.items())[:5]
#         prf_dict.update({query_id : first_five_docs})

#     for id in query_ids:
#         data_combined = []
#         for ele in prf_dict[query_id]:
#             doc_id = ele[0]
#             response = relevant_terms_fetch(INDEX_NAME,doc_id=doc_id)
#             data_combined.append(response)

#         extra_terms = prf_highterm_fetcher(data_combined)

#         # addding the psuedo relevance terms to the existing queries
#         for query in queries:
#             if query[0] == id:  # Check if the current query's ID matches the extra_terms_id
#                 query[1].extend(extra_terms)

#         # same code from queryprocessor to process the queries on the extended terms
#         query_scores = score_generator(queries,document_list,query_ids,attributes_dict,limit)

#         for model in models:
#             filewriter(PRF_OUT_PATH,model,query_ids,query_scores)
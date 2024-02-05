
from tokenizer import porter_processing
from fileparser import documentid_fetcher
from configs import DOC_LIST,INDEX_NAME,models
from vectorProcessors import termvector_driver

def load_queries(QUERY_PATH):
    queries = []
    with open(QUERY_PATH) as f:
        lines = [line.rstrip() for line in f]
        for query in lines:
            if (query):
                id = int(query.split('.')[0])
                content = query.split('.')[1].strip()
                queries.append((id, porter_processing(content,id).split()))
    return queries


def query_driver(QUERY_PATH):

    # get the list of queries which are stored as as a set of tuples(query_id,query as tokens which are word by word)
    queries = load_queries(QUERY_PATH)
    query_ids = [q[0] for q in queries]

    # Fetches the names of the documents from starter files
    document_list = documentid_fetcher(DOC_LIST)

    # Start termvector driver to fetch termvectors and start attributes filling
    termvector_driver(INDEX_NAME,document_list)


    query_scores = { m : {q : { d : "" for d in document_list} for q in query_ids} for m in models}



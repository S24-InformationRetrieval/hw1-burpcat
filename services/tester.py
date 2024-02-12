from tokenizer import porter_processing
from configs import QUERY_PATH
from pprint import pprint

def load_queries(QUERY_PATH):
    queries = []
    with open(QUERY_PATH) as f:
        lines = [line.rstrip() for line in f]
        for query in lines:
            if (query):
                id = int(query.split('.')[0])
                content = query.split('.')[1].strip()
                # queries.append((id, porter_processing(content,"test").split()[2:]))
                queries.append((id, porter_processing(content,"test").split()))
    return queries


queries = load_queries(QUERY_PATH)
pprint(queries)
from configs import QUERY_PATH
from tokenizer import porter_processing

def load_queries():
    queries = []
    with open(QUERY_PATH) as f:
        lines = [line.rstrip() for line in f]
        for query in lines:
            if (query):
                id = int(query.split('.')[0])
                content = query.split('.')[1].strip()
                queries.append((id, porter_processing(content).split()))
    return queries

queries = load_queries()
query_ids = [q[0] for q in queries]
print(queries)
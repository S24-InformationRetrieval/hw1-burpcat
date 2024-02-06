
from tokenizer import porter_processing
from fileparser import documentid_fetcher
from configs import DOC_LIST,INDEX_NAME,models
from vectorProcessors import termvector_driver
from retrievalmodels import retrievalmodel_handler
from indexer import es

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

def score_generator(queries,document_list,query_ids,attributes_dict):

    # generating a dictionary to store the scores for each query on document for every model
    query_scores = { m : {q : { d : "" for d in document_list} for q in query_ids} for m in models}

    cool_list = []
    skank_list = []

    documents_and_documentlength = attributes_dict.get("documents_and_documentlength")

    for model,dsdata in query_scores.items():
        print(f"Generating scores for {model}")

        for query in queries:
            query_id = query[0]
            query_tokens = query[1]
            
            if model=="es":
                es_query = {
                    "query": {
                        "match": {
                        "_content": ' '.join(query_tokens)
                        }
                    },
                    "size" : 1000
                }

                response = es.search(index=INDEX_NAME, body=es_query)

                for doc_id in document_list:
                    query_scores['es'][query_id][doc_id]= "0"

                for hit in response['hits']['hits']:
                    es_docno = hit["_id"]
                    es_score = hit["_score"]
                    print(f"{es_docno}-{es_score}")
                    if es_score != 0:
                        query_scores['es'][query_id][es_docno]= str(es_score)

            else:
                for doc_id in document_list:

                    if not documents_and_documentlength[doc_id] > 0:
                        skank_list.append([query,doc_id])
                        query_scores[model][query_id][doc_id] = "0"
                    else:
                        cool_list.append([query,doc_id])
                        scores = retrievalmodel_handler(model,doc_id,query_tokens,attributes_dict)
                        query_scores[model][query_id][doc_id] = str(scores)
            
        for query_id, docs_scores in query_scores[model].items():
            print(docs_scores)
            # Convert the dictionary to a list of tuples [(doc_id, score), ...] and sort it
            sorted_scores = sorted(docs_scores.items(), key=lambda x: float(x[1]), reverse=True)[:1000]

            # Re-construct the dictionary for this query_id with sorted and trimmed scores
            query_scores[model][query_id] = {doc_id: score for doc_id, score in sorted_scores}
        
    return query_scores


def filewriter(model_name,query_ids,query_scores):
    print(f"Writing output to file for {model_name}")
    filename = f"/home/burpcat/Documents/assignments/ir/hw1-burpcat/outputs/{model_name}_output.txt"
    with open(filename, 'w') as file:
        for ele in query_ids:
            print(model_name,ele)
            rank = 0
            data_to_write = query_scores[model_name][ele]
            for doc_id, score in data_to_write.items():
                rank+=1
                # <query-number> Q0 <docno> <rank> <score> Exp
                file.write(f"{ele} Q0 {doc_id} {rank} {score} Exp\n")


def query_driver(QUERY_PATH):

    # get the list of queries which are stored as as a set of tuples(query_id,query as tokens which are word by word)
    queries = load_queries(QUERY_PATH)
    query_ids = [q[0] for q in queries]

    # Fetches the names of the documents from starter files
    document_list = documentid_fetcher(DOC_LIST)

    # Start termvector driver to fetch termvectors and start attributes filling
    attributes_dict = termvector_driver(INDEX_NAME,document_list)

    query_scores = score_generator(queries,document_list,query_ids,attributes_dict)

    for model in models:
        filewriter(model,query_ids,query_scores)


from elasticsearch import Elasticsearch, exceptions

es = Elasticsearch([{"host":"localhost","port":9200, "scheme": "http"}])
print(f"Elasticsearch instantiated? {es.ping()}")


def start_elastic_service(index_name,corpus,configurations):
    try:

        if es.indices.exists(index=index_name):

            documents_count = es.count(index=index_name)['count']
            decision_state = input(f"Index {index_name} already exits, and documents count is {documents_count}, do you want to reindex (yes/no) ")

            if decision_state == 'yes':
                indexer(index_name, corpus)
            elif decision_state == 'no':
                print("leaving as is cause documents are already indexed")
        else:
            es.indices.create(index=index_name, body=configurations)
            indexer(index_name, corpus)

    except Exception as mainexception:
            print(f"Elasticsearch fails initially, error is {mainexception}")

def indexer(index_name,corpus):
    # This function will index the documents
    count = 0
    for key,value in corpus.items():
        try:
            count+=1
            print(f"{key}-{count}")
            es.index(
                index=index_name,
                id=key,
                document={"_content":value}
            )
        except exceptions.ElasticsearchException as e:
            print(f"Error indexing document {key}: {e}")
from fileparser import start_file_parse
from indexer import start_elastic_service
from queryProcessors import query_driver
from configs import base_string,QUERY_PATH,INDEX_NAME,configurationsv2,configurations

decisionbox = input("1. Start Document Indexing \n2. Start query processing \n3. Create a new index and start query processing \n\nEnter your input (1/2/3):")
if(decisionbox=="1"):
    print("Index creation and updation intialised")
    corpus = start_file_parse(base_string=base_string)
    start_elastic_service(index_name=INDEX_NAME,corpus=corpus,configurations=configurations)
elif(decisionbox=="2"):
    print("Query execution and scoring started")
    query_driver(QUERY_PATH=QUERY_PATH,limit=1000)
elif(decisionbox=='3'):
    print("Index creation and updation intialised")
    corpus = start_file_parse(base_string=base_string)
    start_elastic_service(index_name=INDEX_NAME,corpus=corpus,configurations=configurations)

    print("Query execution and scoring started")
    query_driver(QUERY_PATH=QUERY_PATH,limit=1000)
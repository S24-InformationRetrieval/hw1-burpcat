from fileparser import start_file_parse
from indexer import start_elastic_service
from queryProcessors import query_driver
from configs import base_string,QUERY_PATH,INDEX_NAME,configurationsv2

decisionbox = input("1. Start Document Indexing \n2. Start query processing \n\nEnter your input (1/2):")
if(decisionbox=="1"):
    print("Index creation and updation intialised")
    corpus = start_file_parse(base_string=base_string)
    start_elastic_service(index_name=INDEX_NAME,corpus=corpus,configurations=configurationsv2)
elif(decisionbox=="2"):
    print("Query execution and scoring started")
    query_driver(QUERY_PATH=QUERY_PATH)
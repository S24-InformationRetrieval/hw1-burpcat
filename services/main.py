from fileparser import start_file_parse
from indexer import start_elastic_service

corpus = start_file_parse()
start_elastic_service(index_name="default_index",corpus=corpus)
from fileparser import start_file_parse
from indexer import start_elastic_service
from configs import base_string
from configs import configurations

corpus = start_file_parse(base_string=base_string)
start_elastic_service(index_name="ap89_test",corpus=corpus,configurations=configurations)
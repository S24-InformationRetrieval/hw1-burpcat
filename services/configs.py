base_string = "/home/burpcat/Documents/assignments/ir/hw1-burpcat/IR_data/AP_DATA/ap89_collection"
QUERY_PATH = "/home/burpcat/Documents/assignments/ir/hw1-burpcat/IR_data/AP_DATA/query_desc.51-100.short.txt"
DOC_LIST = "/home/burpcat/Documents/assignments/ir/hw1-burpcat/IR_data/AP_DATA/doclist_new_0609.txt"
INDEX_NAME = "ap89"
models = ['es', 'okapi_tf', 'tfidf', 'okapi_bm25', 'lm_laplace', 'lm_jm']

configurations = {
    "settings" : {
        "number_of_shards": 1,
        "number_of_replicas": 1,
        "analysis": {
            "filter": {
                "english_stop": {
                    "type": "stop",
                    "stopwords_path": "my_stoplist.txt"
                }
            },
            "analyzer": {
                "stopped": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "english_stop"
                    ]
                }
            }
      }
    },
    "mappings": {
        "properties": {
            "content": {
                "type": "text",
                "fielddata": True,
                "analyzer": "stopped",
                "index_options": "positions"
            }
        }
    }
}

configurations_new = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1,
    },
    "mappings": {
        "properties": {
            "content": {
                "type": "text",
                "fielddata": True,
                "index_options": "positions"
            }
        }
    }
    
}

configurations_newv2 = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1,
        "index": {
            "codec": "best_compression"
        }
    },
    "mappings": {
        "properties": {
            "content": {
                "type": "text",
                "fielddata": True,
                "index_options": "positions"
            }
        }
    }
    
}

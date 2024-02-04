base_string = "/home/burpcat/Documents/assignments/ir/hw1-burpcat/IR_data/AP_DATA/ap89_collection"
QUERY_PATH = "/home/burpcat/Documents/assignments/ir/hw1-burpcat/IR_data/AP_DATA/query_desc.51-100.short.txt"

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
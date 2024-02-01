configurations = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1,
        "analysis": {
            "filter": {
                "english_stop": {
                    "type": "stop",
                    "stopwords_path": "my_stoplist.txt"
                },
                "english_stemmer": {
                    "type": "stemmer",
                    "language": "english"
                }
            },
            "analyzer": {
                "stopped_stemmed": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "english_stop",
                        "english_stemmer"  # Adding the stemmer filter here
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
                "analyzer": "stopped_stemmed",  # Use the new analyzer
                "index_options": "positions"
            }
        }
    }
}
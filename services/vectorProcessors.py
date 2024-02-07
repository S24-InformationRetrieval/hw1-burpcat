from indexer import es

def get_term_vectors_batch(index_name, document_list, batch_size):
    responses = []  # List to store responses
    for i in range(0, len(document_list), batch_size):
        batch = document_list[i:i + batch_size]
        print(batch)
        response = es.mtermvectors(index=index_name, term_statistics=True, ids=batch, fields=["_content"])
        responses.append(response)
    return responses

def extracting_termvectors(all_responses):
    documents_and_vectors = {}
    documents_and_documentlength = {}
    term_to_docfrequency = {}
    termtotalfrequency = {}
    terms_list = set()
    missed_docs = []
    
    for ele in all_responses:
        term_vector = ele['docs']
        document_id = term_vector[0]["_id"]

        if "_content" not in term_vector[0]["term_vectors"]:
            documents_and_vectors[document_id] = {}
            documents_and_documentlength[document_id] = 0  # Assuming you want to record a length of 0 for documents without "_content"
            missed_docs.append(document_id)
        else:
            terms = term_vector[0]["term_vectors"]["_content"]["terms"]

            
            for term, details in terms.items():
                term_to_docfrequency[term] = details['doc_freq']
                termtotalfrequency[term] = details['ttf']
                terms_list.add(term)  # Add each term within the loop

            documents_and_vectors[document_id] = terms
            documents_and_documentlength[document_id] = sum(details['term_freq'] for details in terms.values())
        
    return documents_and_vectors,documents_and_documentlength,term_to_docfrequency,termtotalfrequency,terms_list,missed_docs

def calculate_required_vars(documents_and_documentlength,document_list,number_of_documents,terms_list):

    avg_doc_length = sum([documents_and_documentlength[ele] for ele in document_list])  / number_of_documents
    total_doc_length = sum([documents_and_documentlength[ele] for ele in documents_and_documentlength])
    vocab_size = len(terms_list)

    return avg_doc_length,total_doc_length,vocab_size

def termvector_driver(INDEX_NAME,document_list):

    number_of_documents = len(document_list)

    all_responses = get_term_vectors_batch(INDEX_NAME, document_list, batch_size=1)
    print(f"The length of the fetched termvectors is {len(all_responses)}")

    documents_and_vectors,documents_and_documentlength,term_to_docfrequency,termtotalfrequency,terms_list,missed_docs = extracting_termvectors(all_responses)

    avg_doc_length,total_doc_length,vocab_size = calculate_required_vars(documents_and_documentlength,document_list,number_of_documents,terms_list)

    attributes_dict = {"documents_and_vectors": documents_and_vectors,
                       "documents_and_documentlength" : documents_and_documentlength,
                       "term_to_docfrequency": term_to_docfrequency,
                       "termtotalfrequency" : termtotalfrequency ,
                       "terms_list" : terms_list,
                       "missed_docs" : missed_docs,
                       "avg_doc_length" : avg_doc_length,
                       "total_doc_length" : total_doc_length,
                       "vocab_size" : vocab_size,
                       "number_of_documents": number_of_documents}
    
    return attributes_dict
# Return document frequency for a term

def documentfrequency(term,term_to_docfrequency):
    if term in term_to_docfrequency:
        return term_to_docfrequency[term]
    else:
        return 0

# return term frequency for a term
def termfrequency(term,document_id,documents_and_vectors):
    if term in documents_and_vectors[document_id]:
        return documents_and_vectors[document_id][term]['term_freq']
    else:
        return 0
    
# return term frequency in a query
def termfrequency_in_query(term,query):
    return query.count(term)
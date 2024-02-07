from frequencycalcs import termfrequency,termfrequency_in_query,documentfrequency
import numpy as np
from indexer import es

def okapi_tf(word, doc_id,attributes_dict):

    documents_and_vectors = attributes_dict.get("documents_and_vectors")
    documents_and_documentlength = attributes_dict.get("documents_and_documentlength")
    avg_doc_length = attributes_dict.get("avg_doc_length")

    return termfrequency(word,doc_id, documents_and_vectors) / \
    (termfrequency(word,doc_id, documents_and_vectors) + 0.5 + (1.5 * (documents_and_documentlength[doc_id] / avg_doc_length)))

def okapi_score(doc_id, query_tokens,attributes_dict):
    return sum([okapi_tf(word, doc_id,attributes_dict) for word in query_tokens])

def tf_idf(doc_id,query_tokens,attributes_dict):

    # length of documents
    number_of_documents = attributes_dict.get("number_of_documents")
    term_to_docfrequency = attributes_dict.get("term_to_docfrequency")
    score = 0
    for word in query_tokens:
        if documentfrequency(word,term_to_docfrequency) == 0:
            continue
        score += okapi_tf(word,doc_id,attributes_dict) * (np.log10(number_of_documents / documentfrequency(word,term_to_docfrequency)))
    return score

def okapi_bm25(doc_id,query_tokens,attributes_dict):

    k1 = 1.2 # higher number accounts for saturation less
    k2 = 1000 # weight query term frequency, how many times does w appear in query, higher tf_q, more important
    b = 0.3 # (0, 1) larger value penalizes longer documents

    score = 0

    number_of_documents = attributes_dict.get("number_of_documents")
    documents_and_documentlength = attributes_dict.get("documents_and_documentlength")
    avg_doc_length = attributes_dict.get("avg_doc_length")
    term_to_docfrequency = attributes_dict.get("term_to_docfrequency")
    documents_and_vectors = attributes_dict.get("documents_and_vectors")

    for word in query_tokens:
        t1 = np.log10((number_of_documents + 0.5) / (0.5 + documentfrequency(word,term_to_docfrequency)))
        
        t2_num = termfrequency(word,doc_id, documents_and_vectors) +  k1 + termfrequency(word,doc_id, documents_and_vectors)
        t2_denom = termfrequency(word,doc_id, documents_and_vectors) + k1 * ((1 - b) + b * (documents_and_documentlength[doc_id] / avg_doc_length))
        t2 = t2_num / t2_denom
        
        t3 = (termfrequency_in_query(word,query_tokens) + k2 * termfrequency_in_query(word,query_tokens)) / (termfrequency_in_query(word,query_tokens) + k2)
        
        score += (t1 * t2 * t3)
    return score

def p_laplace(word, doc_id,attributes_dict):

    documents_and_documentlength = attributes_dict.get("documents_and_documentlength")
    vocab_size = attributes_dict.get("vocab_size")
    documents_and_vectors = attributes_dict.get("documents_and_vectors")

    return (termfrequency(word,doc_id, documents_and_vectors) + 1) / (documents_and_documentlength[doc_id] + vocab_size)


def unigramlm_laplacesmoothing(doc_id,query_tokens,attributes_dict):

    documents_and_vectors = attributes_dict.get("documents_and_vectors")

    score = 0
    for word in query_tokens:
        if termfrequency(word,doc_id, documents_and_vectors) != 0:
            score += np.log10(p_laplace(word, doc_id, attributes_dict))
        else:
            score -= 1000
    return score

def p_jm(word, doc_id,attributes_dict):

    documents_and_documentlength = attributes_dict.get("documents_and_documentlength")
    termtotalfrequency = attributes_dict.get("termtotalfrequency")
    total_doc_length = attributes_dict.get('total_doc_length')
    documents_and_vectors = attributes_dict.get("documents_and_vectors")

    lmda = 0.9 # (0, 1), higher value better for short queries, foreground vs background prob weights
    t1 = lmda * (termfrequency(word,doc_id, documents_and_vectors) / documents_and_documentlength[doc_id])
    
    t2 = (1 - lmda) * (termtotalfrequency[word] / total_doc_length)
    
    return t1 + t2


def unigramlm_jelinekmercer(doc_id,query_tokens,attributes_dict):
    documents_and_vectors = attributes_dict.get("documents_and_vectors")
    score = 0
    for word in query_tokens:
        if termfrequency(word,doc_id, documents_and_vectors) != 0:
            score += np.log10(p_jm(word, doc_id, attributes_dict))
        else:
            score -= 1000
    return score

# append all the attributes to a list or smh, and then create a retrieval model handling function
# which takes in all the parameters and returns the values of the appropriate

def retrievalmodel_handler(model,doc_id,query_tokens,attributes_dict):
        
        model_handler = {'okapi_tf' : okapi_score, 'tfidf' : tf_idf, 'okapi_bm25' : okapi_bm25, 'lm_laplace' : unigramlm_laplacesmoothing, 'lm_jm' : unigramlm_jelinekmercer}
        documents_and_vectors = attributes_dict.get("documents_and_vectors")
        documents_and_documentlength = attributes_dict.get("documents_and_documentlength")
        term_to_docfrequency = attributes_dict.get("term_to_docfrequency")
        termtotalfrequency = attributes_dict.get("termtotalfrequency")
        terms_list = attributes_dict.get("terms_list")
        missed_docs = attributes_dict.get("missed_docs")
        avg_doc_length = attributes_dict.get("avg_doc_length")
        total_doc_length = attributes_dict.get('total_doc_length')
        vocab_size = attributes_dict.get("vocab_size")

        scores = model_handler[model](doc_id,query_tokens,attributes_dict)

        return scores


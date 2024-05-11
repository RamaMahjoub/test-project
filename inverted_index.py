from typing import Dict
import math
from text_proccessing import _get_proccessed_text
from collections import defaultdict
import shelve


def create_inverted_index(cleaned_tokens:list):
    index=defaultdict(list)
    for item in cleaned_tokens:
        unique_tokens=set(item["tokens"])
        for token in unique_tokens:
            index[token].append(item["id"])
    return dict(index)


def calculate_tf(doc_tokens:list):
    tf = {}
    for term in doc_tokens:
        tf[term] = (doc_tokens.count(term) / len(doc_tokens)) 
    return tf

def calculate_idf(inverted_index:Dict[str,str],docs_count:int):
    idf = {}
    for term, doc_ids in inverted_index.items():
        idf[term] = math.log((docs_count / len(doc_ids)) + 1,10)
    
    return idf


def calculate_tf_idf(doc_tokens:list,idf:Dict[str,str]):
    tf_idf={}
    doc_tf=calculate_tf(doc_tokens)
    
    for term in doc_tokens:    
        tf_idf[term] = doc_tf[term] * idf[term]
    return tf_idf


def _create_docs_vectors(cleaned_tokens):
    vectors={}

    index=create_inverted_index(cleaned_tokens)
    # print(index)
    idf=calculate_idf(index,len(cleaned_tokens))
    for item in cleaned_tokens:
        vectors[item["id"]]= calculate_tf_idf(item["tokens"],idf)

    with shelve.open('db/' + 'dataset_name' + '_documents_vector',flag='c') as db:
        db["documents_vector"] = vectors
    return vectors



def create_weighted_inverted_index(cleaned_tokens) -> None:

    weighted_inverted_index = defaultdict(list)
    vectors = _create_docs_vectors(cleaned_tokens)
    for doc_id, doc_weighted_terms in vectors.items():
        for term, weight in doc_weighted_terms.items():
            weighted_inverted_index[term].append({doc_id: weight})
    with shelve.open('db/' + "dataset_name" + '_inverted_index.db',flag='c') as db:
        # Store the inverted index in the "shelve" file
        db['inverted_index'] = weighted_inverted_index
    





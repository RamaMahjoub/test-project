import ir_datasets
from storing_and_loading import load_file
from sklearn.metrics.pairwise import cosine_similarity
import csv
import codecs
from gensim.models.doc2vec import Doc2Vec
from text_proccessing import _get_words_tokenize
from gensim.models import Word2Vec
from text_proccessing import _get_proccessed_text_recreation,_get_proccessed_text_science
from matching_and_ranking import get_global_matrix,get_global_vectorizer,create_query_vector


def _get_queries(dataset_name:str,queries_type:str):
    queries_subset = ir_datasets.load("lotte/"+dataset_name+"/dev/"+queries_type)
    tsv_path = queries_subset.queries_path()
    queries={}
    # Open the TSV file with the correct encoding
    with codecs.open(tsv_path, 'r', encoding='utf-8') as tsv_file:
        # Create a CSV reader for TSV files
        reader = csv.reader(tsv_file, delimiter='\t')
        queries={row[0]:row[1] for row in reader}
        # i=0
        # for row in reader:
        #     queries[row[0]]=row[1]
        #     if i==10:
        #         break
        #     i+=1
        # queries={id:text for id,doc in search_subset.queries_iter()}
    return queries


def search(query_vector: str,vectore_matrix,doc_ids):
    similarity_threshold=0.05
    similarity_matrix = cosine_similarity(query_vector,vectore_matrix)
    document_ranking = dict(zip(doc_ids, similarity_matrix.flatten()))
    filtered_documents = {key: value for key, value in document_ranking.items() if value >= similarity_threshold}
    sorted_dict = sorted(filtered_documents.items(), key=lambda item: item[1], reverse=True)
    return  sorted_dict


# def create_query_vector(vectorizer,query:str):
#     print("query: ",query)
#     return vectorizer.transform([query])
    

#for us
def get_queries_answers(dataset_name:str,type:str,crawling:bool):
    queries = _get_queries(dataset_name,type)
    queries_answers={}
    vectore_matrix=get_global_matrix(dataset_name,crawling)
    vectorizer = get_global_vectorizer(dataset_name,crawling)
    doc_ids = load_file("db/"+dataset_name+"/topic_detiction/keys_id.bin")

    for id,query in list(queries.items()):
        print("your question is: " + id)
        query_vector=create_query_vector(dataset_name,query,crawling)
        top_related_docs = search(query_vector,vectore_matrix,doc_ids)
        queries_answers[id]=top_related_docs
        print(len(top_related_docs))
    return queries_answers


# def search_with_embeding(dataset_name:str,query:str,items,model):
#     similarity_threshold=0.3
#     top_n=len(items.items())
    
#     if dataset_name=="science":
#         query_vector = model.infer_vector(_get_words_tokenize(_get_proccessed_text_science(query)))
#     else:
#         query_vector = model.infer_vector(_get_words_tokenize(_get_proccessed_text_recreation(query)))

#     similar_docs = model.docvecs.most_similar([query_vector], topn=top_n)
    
#     return [ doc for doc in similar_docs if doc[1]>=similarity_threshold ]


# def get_queries_answer_with_embeding(dataset_name:str,items,type:str):
#     queries = _get_queries(dataset_name,type)
#     queries_answers={}
#     print("loading..")
#     model=Doc2Vec.load("db/"+dataset_name+"/doc2vec_model")
#     print("loading done..")
#     for id,query in list(queries.items()):
#         print("your question is: " + id)
#         top_related_docs = search_with_embeding(dataset_name,query,items,model)
#         queries_answers[id]=top_related_docs
#     return queries_answers
    

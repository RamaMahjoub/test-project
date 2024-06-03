from text_proccessing import _get_proccessed_text_science,_get_proccessed_text_recreation
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from storing_and_loading import store_file


def get_corpus(dataset_name:str,crawling:bool):
    if dataset_name=="science":
        if crawling:
            dataset = pd.read_csv(r"E:\University\Fifth_year\IR\lotte\science\dev\crawling_collection.tsv",sep='\t', header=None)
            corpus={str(row[0]):row[1] for index,row in dataset.iterrows()}
        else: 
            dataset = pd.read_csv(r"C:\Users\alaaK\.ir_datasets\lotte\lotte_extracted\lotte\science\dev\collection.tsv",sep='\t', header=None)
            corpus={str(row[0]):row[1] for index,row in dataset.iterrows()}
    else:
        if crawling :
            dataset = pd.read_csv(r"E:\University\Fifth_year\IR\lotte\recreation\dev\crawling_collection.tsv",sep='\t', header=None)
            corpus={str(row[0]):row[1] for index,row in dataset.iterrows()}
        else:
            dataset = pd.read_csv(r"C:\Users\alaaK\.ir_datasets\lotte\lotte_extracted\lotte\recreation\dev\collection.tsv",sep='\t', header=None)
            corpus={str(row[0]):row[1] for index,row in dataset.iterrows()}
    return corpus


def create_vector(dataset_name:str):
    corpus=get_corpus(dataset_name,False)
    if dataset_name=="science":
        # " gjernokekp   http //  ( rdhgfkdkfpe, f)"
        #     5              6           10              => [ [ 5 , 6 , 10  ] , [  5 , 5 ,5 ] ] 
        #   query                                        =>   [ 3  , 7  , 9 ]
        vectorizer = TfidfVectorizer(preprocessor=_get_proccessed_text_science)
    else:
        vectorizer = TfidfVectorizer(preprocessor=_get_proccessed_text_recreation)

    # Fit the vectorizer to the documents
    tfidf_matrix = vectorizer.fit_transform(list(corpus.values()))
    
    # tfidf_matrix.getrow()
    store_file('db/'+dataset_name+'/vectore_matrix.bin',tfidf_matrix)
    store_file('db/'+dataset_name+'/vectorizer_model.bin',vectorizer)


def create_crawling_vector (dataset_name:str,path:str):
    print("corpus start ..")
    corpus=get_corpus(path,True)
    print("corpus done ..")
    print("vectorizer start ..")
    if dataset_name=="science":
        vectorizer = TfidfVectorizer(preprocessor=_get_proccessed_text_science)
    else:
        vectorizer = TfidfVectorizer(preprocessor=_get_proccessed_text_recreation)
    print("vectorizer done ..")
    # Fit the vectorizer to the documents
    tfidf_matrix = vectorizer.fit_transform(list(corpus.values()))
    # tfidf_matrix.getrow()
    print("tfidf_matrix start ..")
    store_file('db/'+dataset_name+'/crawling/vectore_matrix.bin',tfidf_matrix)
    store_file('db/'+dataset_name+'/crawling/vectorizer_model.bin',vectorizer)
    print("tfidf_matrix done ..")
    
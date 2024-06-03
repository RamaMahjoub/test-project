from sklearn.metrics.pairwise import cosine_similarity
from storing_and_loading import load_file
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


_science_corpus = None
_science_matrex = None
_science_vectorizer = None
_recreation_corpus = None
_recreation_matrex = None
_recreation_vectorizer = None
_crawling_science_matrex = None
_crawling_science_vectorizer = None


def get_corpus(dataset_name:str):
    if dataset_name=="science":
        dataset = pd.read_csv(r"C:\Users\alaaK\.ir_datasets\lotte\lotte_extracted\lotte\science\dev\collection.tsv",sep='\t', header=None)
        corpus={str(row[0]):row[1] for index,row in dataset.iterrows()}
        return corpus
    else:
        dataset = pd.read_csv(r"C:\Users\alaaK\.ir_datasets\lotte\lotte_extracted\lotte\recreation\dev\collection.tsv",sep='\t', header=None)
        corpus={str(row[0]):row[1] for index,row in dataset.iterrows()}
        return corpus

def get_corpus_from_path(path:str):
    dataset = pd.read_csv(path,sep='\t', header=None)
    corpus={str(row[0]):row[1] for index,row in dataset.iterrows()}
    return corpus


def set_inverted_index_store_global_variables():
    global _science_matrex
    global _science_vectorizer
    global _recreation_matrex
    global _recreation_vectorizer
    global _science_corpus
    global _recreation_corpus
    
    _science_corpus=get_corpus("science")
    print("science: ",len(_science_corpus.keys()))
    _recreation_corpus=get_corpus("recreation")
    print("recreation: ",len(_recreation_corpus.keys()))

    # science
    _science_matrex=load_file('db/science/vectore_matrix.bin')
    _science_vectorizer = load_file('db/science/vectorizer_model.bin')
    
    #recreation
    _recreation_matrex=load_file('db/recreation/vectore_matrix.bin')
    _recreation_vectorizer = load_file('db/recreation/vectorizer_model.bin')
    
# def set_cprpus_global_variable():
#     global _science_corpus
#     global _recreation_corpus
    
#     _science_corpus=get_corpus("science")
#     print("science: ",len(_science_corpus.keys()))
#     _recreation_corpus=get_corpus("recreation")
#     print("recreation: ",len(_recreation_corpus.keys()))


def set_crawling():
    global _crawling_science_matrex
    global _crawling_science_vectorizer
    # science
    _crawling_science_matrex=load_file('db/science/crawling/vectore_matrix.bin')
    _crawling_science_vectorizer = load_file('db/science/crawling/vectorizer_model.bin')
    


def related_docs(dataset_name,top_related_docs):
    corpus= get_global_corpus(dataset_name)
    
    ans=[ dict(id=str(doc[0]),content=corpus[str(doc[0])]) for doc in top_related_docs[:20] if str(doc[0]) in corpus.keys()]
    return ans


def search(query_vector,vectore_matrix,doc_ids):
    similarity_threshold=0.02
    print("seaaaaaaaaaaaaaaarsh")
    similarity_matrix = cosine_similarity(query_vector,vectore_matrix)
    document_ranking = dict(zip(list(doc_ids), similarity_matrix.flatten()))
    filtered_documents = {key: value for key, value in document_ranking.items() if value >= similarity_threshold}
    sorted_dict = sorted(filtered_documents.items(), key=lambda item: item[1], reverse=True)
    return sorted_dict 


def create_query_vector(dataset_name:str,query:str,crawling:bool):
    print("query: ",query)

    # tfidf_matrix = vectorizer.transform([query])
    # return tfidf_matrix
    return get_global_vectorizer(dataset_name,crawling).transform([query]) # [ [5 ,5 , 5 ]  ]


app = FastAPI()
origins = [
    "http://localhost:10000",  # Your frontend URL
    "http://127.0.0.1:10000"  # Sometimes, the frontend may use this URL
]

# Add CORSMiddleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/search")
def ranking(dataset_name,query,crawling:bool):
    query_vector=create_query_vector(dataset_name,query,crawling) 
    matrix=get_global_matrix(dataset_name,crawling) 
    
    doc_ids =load_file("db/"+dataset_name+"/keys_id.bin")
    print("hi" ,list(doc_ids)[:10])
    top_related_docs=search(query_vector,matrix,doc_ids)
    docs_contecnt=related_docs(dataset_name,top_related_docs)
    print(len(top_related_docs))
    
    return docs_contecnt[:15]


def get_global_corpus(dataset_name: str):
    
    return globals()["_" + dataset_name + "_corpus"]


def get_global_vectorizer(dataset_name: str,crawling:bool):
    if crawling:
        return globals()["_crawling_" + dataset_name + "_vectorizer"]
    else:
        return globals()["_" + dataset_name + "_vectorizer"]
    

def get_global_matrix(dataset_name: str,crawling:bool):
    if crawling:
        return globals()["_crawling_" + dataset_name + "_matrex"]
    else:
        return globals()["_" + dataset_name + "_matrex"]



@app.on_event("startup")
async def on_startup():
    print("init start ...")
    set_inverted_index_store_global_variables()
    # set_cprpus_global_variable()
    set_crawling()
    print("init done ...")

    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
from gensim.models.doc2vec import Doc2Vec,TaggedDocument
from text_proccessing import _get_proccessed_text_science,_get_words_tokenize,_get_proccessed_text_recreation
from inverted_index import get_corpus
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from storing_and_loading import load_file
from matching_and_ranking import get_global_corpus

_science_corpus = None
_science_model = None
_recreation_corpus = None
_recreation_model = None


def set_global_variable():
    global _science_corpus 
    global _science_model 
    global _recreation_corpus 
    global _recreation_model 
    
    _science_corpus=get_corpus("science",False)
    _science_model=Doc2Vec.load("db/science/embedding/doc2vec_model")

    _recreation_corpus=get_corpus("recreation",False)
    _science_model=Doc2Vec.load("db/recreation/embedding/doc2vec_model")
    
    


def init_docs(dataset_name:str):
    items= get_corpus(dataset_name,False)
    if dataset_name=="science":
        documents=[ TaggedDocument(words=_get_words_tokenize(_get_proccessed_text_science(item[1])), tags=[item[0]]) for item in list(items.items())]
    else:
        documents=[ TaggedDocument(words=_get_words_tokenize(_get_proccessed_text_recreation(item[1])), tags=[item[0]]) for item in list(items.items())]
    return documents

def embedding_model(dataset_name:str, documents):
    model = Doc2Vec(vector_size=1000,  # Dimensionality of the document vectors
                    window=3,        # Maximum distance between the current and predicted word within a sentence
                    min_count=1,      # Ignores all words with total frequency lower than this
                    workers=6,        # Number of CPU cores to use for training
                    epochs=20)        # Number of training epochs

    model.build_vocab(documents)
    model.train(documents, total_examples=model.corpus_count, epochs=model.epochs)
    model.save("db/"+dataset_name+"/embedding/doc2vec_model")


# dataset_name="science"
# documents=init_docs(dataset_name)
# embedding_model(dataset_name,documents)


def related_docs(dataset_name,top_related_docs):
    corpus= get_global_corpus(dataset_name)
    
    ans=[ dict(id=str(doc[0]),content=corpus[str(doc[0])]) for doc in top_related_docs[:20] if str(doc[0]) in corpus.keys()]
    return ans


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


def search(dataset_name:str,query:str,items,model):
    similarity_threshold=0.3
    top_n=len(items.items())
    
    if dataset_name=="science":
        query_vector = model.infer_vector(_get_words_tokenize(_get_proccessed_text_science(query)))
    else:
        query_vector = model.infer_vector(_get_words_tokenize(_get_proccessed_text_recreation(query)))

    similar_docs = model.docvecs.most_similar([query_vector], topn=top_n)
    
    return [ doc for doc in similar_docs if doc[1]>=similarity_threshold ]



@app.get("/search")
def ranking(dataset_name,query):
    
    doc_ids =load_file("db/"+dataset_name+"/topic_detiction/keys_id.bin")
    print("hi" ,list(doc_ids)[:10])
    top_related_docs=search(dataset_name,query,doc_ids)
    docs_contecnt=related_docs(dataset_name,top_related_docs)
    print(len(top_related_docs))
    
    return docs_contecnt[:15]


@app.on_event("startup")
async def on_startup():
    print("init start ...")
    set_global_variable()
    print("init done ...")

    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
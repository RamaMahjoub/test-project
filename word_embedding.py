from gensim.models.doc2vec import Doc2Vec,TaggedDocument
from text_proccessing import _get_proccessed_text_science,_get_words_tokenize,_get_proccessed_text_recreation
from inverted_index import get_corpus
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from storing_and_loading import load_file

_science_model = None
_recreation_model = None
_science_corpus = None
_recreation_corpus = None

def set_global_variable():
    global _science_model 
    global _recreation_model 
    global _science_corpus
    global _recreation_corpus
    
    _science_corpus=get_corpus("science",False)

    _recreation_corpus=get_corpus("recreation",False)

    _science_model=Doc2Vec.load("db/science/embedding/doc2vec_model")

    _recreation_model=Doc2Vec.load("db/recreation/embedding/doc2vec_model")
    
    


def init_docs(dataset_name:str):
    items= get_corpus(dataset_name,False)
    if dataset_name=="science":
        documents=[ TaggedDocument(words=_get_words_tokenize(_get_proccessed_text_science(item[1])), tags=[item[0]]) for item in list(items.items())]
    else:
        documents=[ TaggedDocument(words=_get_words_tokenize(_get_proccessed_text_recreation(item[1])), tags=[item[0]]) for item in list(items.items())]
    return documents

def embedding_model(dataset_name:str, documents):
    model = Doc2Vec(vector_size=1000,  # Dimensionality of the document vectors
                    window=3,         # Maximum distance between the current and predicted word within a sentence
                    min_count=1,      # Ignores all words with total frequency lower than this
                    workers=6,        # Number of CPU cores to use for training
                    epochs=20)        # Number of training epochs

    model.build_vocab(documents)
    model.train(documents, total_examples=model.corpus_count, epochs=model.epochs)
    model.save("db/"+dataset_name+"/embedding/doc2vec_model")




def related_docs(dataset_name,top_related_docs):
    corpus= get_global_corpus(dataset_name)
    # print("hi from here:",corpus)
    ans=[]
    for doc in top_related_docs[:20]:
        # print("id: ",doc[0])
        # print("content:",corpus[str(doc[0])])
        ans.append(dict(id=str(doc[0]),content=corpus[str(doc[0])]))
    # ans=[ dict(id=str(doc[0]),content=corpus[str(doc[0])]) for doc in top_related_docs if str(doc[0]) in corpus.keys()]
    print("ans: ",len(ans))
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
    top_n=len(items)
    if dataset_name=="science":
        query_vector = model.infer_vector(_get_words_tokenize(_get_proccessed_text_science(query)))
    else:
        query_vector = model.infer_vector(_get_words_tokenize(_get_proccessed_text_recreation(query)))

    similar_docs = model.docvecs.most_similar([query_vector], topn=top_n)
    print("hiiiiiiiiiiiiiii")
    return [ doc for doc in similar_docs if doc[1]>=similarity_threshold ]



@app.get("/search")
def ranking(dataset_name,query):
    print("start searhhhhhhhhhhhhhhhhhhhhhhhhhhh")
    doc_ids =load_file("db/"+dataset_name+"/keys_id.bin")
    model=get_global_model(dataset_name)
    print("model",model)
    top_related_docs=search(dataset_name,query,doc_ids,model)
    docs_contecnt=related_docs(dataset_name,top_related_docs)
    print(len(top_related_docs))
    
    return docs_contecnt




def get_global_model(dataset_name:str,):
    return globals()["_" + dataset_name + "_model"]

def get_global_corpus(dataset_name:str,):
    return globals()["_" + dataset_name + "_corpus"]



@app.on_event("startup")
async def on_startup():
    print("init start ...")
    set_global_variable()
    print("init done ...")

    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
from inverted_index import create_vector
from word_embedding import init_docs,embedding_model


#create tf idf vectorizer fpr science dataset
create_vector("science")
#create embedding model for science dataset
documents=init_docs("science")
embedding_model("science",documents)


#create tf idf vectorizer fpr recreation dataset
create_vector("recreation")
#create embedding model for science dataset
documents=init_docs("recreation")
embedding_model("recreation",documents)


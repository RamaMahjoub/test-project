import pickle

def store_file(path:str, content):      
    with open(path, 'wb') as file:
        pickle.dump(content, file)

def load_file(path:str):
    with open(path, 'rb') as file:
        return pickle.load(file)
        


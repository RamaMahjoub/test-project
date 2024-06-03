# Information Retrieval System

***

A university project that uses two datasets from [ir-datasets](https://ir-datasets.com/) and build a search engine on them using Python and Flask.

## Datasets

- [**Sience**](https://ir-datasets.com/lotte.html#lotte/science/dev).

- [**Recreation**](https://ir-datasets.com/lotte.html#lotte/recreation/dev).


## How to use the search engine?

After running your project locally you can perform your query and get the results of the chosen dataset easily with a [simple Vue web app](https://google.com).


## How to run the project?

Install required packages. 
Run db_factory.py file for the first time to set the database on your device.

## Services


*note that service might behave differently based on the selected dataset*
*Each service runs on a separate port*

- **Search**:

you have to run a service by this command:

    - fastapi run matching_and_ranking.py --reload --port 8001

Performs search query and get full documnents results based on passed query and dataset passed.

the following APIs runs the search service on our project:

    - GET: 8001:/search?query="YOUR-QUERY"&dataset="science/recreation"&crawling=true/false
the "crawling=true/false" is available just on science dataset


- **Text Processing**:

you have to run a service by this command:

    - fastapi run text_proccessing.py --reload --port 8000

The implemented text processing steps are:


1. **Remove urls**


2. **Remove punctuations**


3. **Tokenizing**


3. **Lowerization**


5. **Cleaning**


6. **limitization**

the following API runs the text processing service on the provided text and dataset:

    - GET: 8000:/process-text?text="YOUR-TEXT"&dataset="science/recreation"


- **Query Suggestions** :

you have to run a service by this command:

    - fastapi run query_refinement.py --reload --port 8002

Performs a query suggestions search and returns ranked suggestions to the given query and dataset.

the following API runs the Query Suggestions service:

    - GET: 8002:/suggestions?query="YOUR-QUERY"&dataset="science/recreation"


- **Embedding** :

you have to run a service by this command:

    - fastapi run word_embedding.py --reload --port 8003

Performs search by embedding model query and get full documnents results based on passed query and dataset passed.

the following API runs search service by embedding on our project:

    - GET: :8003/search?query="YOUR-QUERY"&dataset="science/recreation"


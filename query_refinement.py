import shelve
from collections import Counter
import ir_datasets
from nltk.corpus import words
from spellchecker import SpellChecker
from storing_and_loading import store_file,load_file
from query_proccessing import _get_queries
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

_recreation_queries = set()  # empty set
_science_queries = set()  # empty set
 

def set_query_refinement_global_variables() -> None:
    print("set up")
    global _recreation_queries
    global _science_queries

    ############## recreation ##############
    #{ "1":"value"}
    forum_generic_recreation_queries = set(_get_queries("recreation","forum").values())
    search_generic_recreation_queries = set(_get_queries("recreation","search").values())
    
    forum_recreation_queries = set(query for query in forum_generic_recreation_queries)
    search_recreation_queries = set(query for query in search_generic_recreation_queries)
    _recreation_queries = forum_recreation_queries.union(search_recreation_queries)

    ############## Science ##############
    forum_generic_science_queries = set(_get_queries("science","forum").values())
    search_generic_science_queries = set(_get_queries("science","search").values())
    
    forum_science_queries = set(query for query in forum_generic_science_queries)
    search_science_queries = set(query for query in search_generic_science_queries)
    _science_queries = forum_science_queries.union(search_science_queries)


def _get_query_suggestions(query: str, dataset_name: str) -> list:
    global _recreation_queries
    global _science_queries

    if dataset_name == 'recreation':
        queries = _recreation_queries
    else:
        queries = _science_queries

    suggestions = []
    # [ " one" , "two"]
    query_terms = query.lower().split()
    query_freq = Counter(query_terms)

    for suggest_query in queries:
        suggest_query_terms = suggest_query.lower().split()
        if set(query_terms).intersection(set(suggest_query_terms)):
            freq = sum([query_freq[term] for term in set(query_terms) & set(suggest_query_terms)])
            suggestions.append((suggest_query, freq))

    return suggestions


def _get_ranked_suggestion(suggestions: list) -> list:
    ranked_suggestions = sorted(suggestions, key=lambda x: -x[1])
    return [suggestion[0] for suggestion in ranked_suggestions]


def _suggest_corrected_query(text: str):
    spell = SpellChecker()

    word_set = set(words.words())

    # Create a list to store the corrected tokens
    corrected_tokens = []

    # [Spell ,check, each ,token]
    
    for token in text.split():
        if token in word_set:
            corrected_tokens.append(token)
        else:
            suggestions = spell.candidates(token)
            if suggestions:
                corrected_tokens.append(spell.correction(token))
            else:
                corrected_tokens.append(token)

    return ' '.join(corrected_tokens)

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


@app.get("/suggestions")
def get_ranked_query_suggestions(query: str, dataset_name: str):
    corrected_query = _suggest_corrected_query(query)
    suggestions = _get_query_suggestions(corrected_query, dataset_name)
    ranked_suggestions = _get_ranked_suggestion(suggestions)
    ranked_suggestions.insert(0, corrected_query)
    return ranked_suggestions[:15]


@app.on_event("startup")
async def on_startup():
    print("init start ...")
    set_query_refinement_global_variables()
    print("init done ...")

    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
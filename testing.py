# from spellchecker import SpellChecker
# from nltk.tokenize import word_tokenize
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from text_proccessing import _get_proccessed_text

# def spell_check(text):
#     spell = SpellChecker()

#     # Tokenize the text
#     tokens = word_tokenize(text)

#     # Find misspelled words
#     misspelled = spell.unknown(tokens)

#     # Generate and rank correction suggestions
#     corrections = {}
#     for word in misspelled:
#         # Generate candidate corrections
#         candidates = spell.candidates(word)
#         # Rank the candidates based on their frequency
#         ranked_candidates = spell.correction(word)
#         corrections[word] = ranked_candidates

#     # Generate corrected text
#     corrected_tokens = [corrections.get(word, word) for word in tokens]

#     return corrected_tokens

# # Example usage
# input_text = "Ths quick browm fox jummped ovre the lazzy dog."
# corrected_text = spell_check(input_text)
# print(corrected_text)

corpus = {
    "doc_1": "Software engineering at Damascus university Software",
    "doc_2": "Information retrieval at Damascus university",
    "doc_3": "Indexing Information retrieval"
}
documents = list(corpus.values())

# TODO : ADD YOUR OWN TOKENIZER & PREPROCESSOR !

vectorizer = TfidfVectorizer(preprocessor=_get_proccessed_text)
tfidf_matrix = vectorizer.fit_transform(documents)
print(tfidf_matrix)
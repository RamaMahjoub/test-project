from spellchecker import SpellChecker
from datetime import datetime
from nltk.corpus import stopwords, words
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize

def _get_words_tokenize(text: str) -> list:

    return word_tokenize(text)

def _filter_tokens(tokens: list) -> list:

    stop_words = set(stopwords.words('english'))

    filtered_tokens = [token for token in tokens if token not in stop_words]

    return filtered_tokens

def _remove_punctuations(text: str) -> list:

    tokenizer = RegexpTokenizer(r'\w+')
    non_punctuations_tokens = tokenizer.tokenize(text)
    return non_punctuations_tokens

def _lowercase_tokens(tokens: list) -> list:

    return [token.lower() for token in tokens]

def _lemmatize_tokens(tokens: list) -> list:
 
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmatized_tokens

def _stem_tokens(tokens: list) -> list:
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return stemmed_tokens

def spell_check(tokens: list):
    spell = SpellChecker()

    misspelled = spell.unknown(tokens)

    corrections = {}
    for word in misspelled:
        ranked_candidates = spell.correction(word)
        corrections[word] = ranked_candidates

    corrected_tokens = [corrections.get(word, word) for word in tokens]

    return corrected_tokens
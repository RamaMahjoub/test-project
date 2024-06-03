# from spellchecker import SpellChecker
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import re
from nltk.corpus import wordnet
from nltk import pos_tag

# api
def _get_proccessed_text_science( text:str) ->list:
    # print("1111111111111111111111111111111")
    text_without_urls=remove_urls(text)
    text_without_punctuation=_remove_punctuations(text_without_urls)
    tokens=_get_words_tokenize(text_without_punctuation)
    lowercase_tokens=_lowercase_tokens(tokens)
    temp_dataset=normalize_elements(lowercase_tokens)
    tokens_without_stopwords=_remove_stopwords(temp_dataset)
    # stemed_tokens=_stem_tokens(tokens_without_stopwords)
    limitized_tokens=preprocess_and_lemmatize(tokens_without_stopwords)
    return ' '.join(limitized_tokens)

# api
def _get_proccessed_text_recreation( text:str) ->list:
    
    text_without_urls=remove_urls(text)
    text_without_punctuation=_remove_punctuations(text_without_urls)
    tokens=_get_words_tokenize(text_without_punctuation)
    lowercase_tokens=_lowercase_tokens(tokens)
    tokens_without_stopwords=_remove_stopwords(lowercase_tokens)
    # stemed_tokens=_stem_tokens(tokens_without_stopwords)
    limitized_tokens=preprocess_and_lemmatize(tokens_without_stopwords)
    return ' '.join(limitized_tokens)


def _get_foreign_characters_filtered_tokens(terms):
   
    clean_list = [x for x in terms if all(c in string.printable for c in x)]
    return clean_list

def _get_words_tokenize(text: str) -> list:

    return word_tokenize(text)

def _remove_stopwords(tokens: list) -> list:

    stop_words = set(stopwords.words('english'))

    tokens_without_stopwords = [token for token in tokens if token not in stop_words]

    return tokens_without_stopwords

def _remove_punctuations(text: str) -> list:

    # define the regular expression pattern
    pattern = r"(?<!\d)\.(?!\d)|[^\w\s.]"

    # Remove punctuation using the pattern
    cleaned_text =  re.sub(pattern," ", text)

    return cleaned_text
    # tokenizer = RegexpTokenizer(r'\w+')
    # non_punctuations_tokens = tokenizer.tokenize(text)
    # return non_punctuations_tokens


def remove_urls(text):
    """Remove URLs from a given text string."""
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)



def _lowercase_tokens(tokens: list) -> list:

    return [token.lower() for token in tokens]


def get_wordnet_pos(word):
    tag = pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    
    return tag_dict.get(tag, wordnet.NOUN)

def preprocess_and_lemmatize(tokens):
    """Tokenize, POS tag, and lemmatize the input text."""
    lemmatizer = WordNetLemmatizer()
    pos_tagged_tokens = pos_tag(tokens)  # POS tag tokens
    lemmatized_tokens = [lemmatizer.lemmatize(token, get_wordnet_pos(token)) for token, tag in pos_tagged_tokens]
    return lemmatized_tokens

def _stem_tokens(tokens: list) -> list:
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return stemmed_tokens

# def spell_check(tokens: list):
#     spell = SpellChecker()

#     misspelled = spell.unknown(tokens)

#     corrections = {}
#     for word in misspelled:
#         ranked_candidates = spell.correction(word)
#         corrections[word] = ranked_candidates

#     corrected_tokens = [corrections.get(word, word) for word in tokens]

#     return corrected_tokens



# function to normalize chemical elements in a text
def normalize_elements(tokens):
    
    element_dict = {
    'h': 'hydrogen', 'he': 'helium', 'li': 'lithium', 'be': 'beryllium',
    'b': 'boron', 'c': 'carbon', 'n': 'nitrogen', 'o': 'oxygen', 'f': 'fluorine', 'ne': 'neon',
    'na': 'sodium', 'mg': 'magnesium', 'al': 'aluminium', 'si': 'silicon', 'p': 'phosphorus',
    's': 'sulfur', 'cl': 'chlorine', 'ar': 'argon', 'k': 'potassium', 'ca': 'calcium',
    'sc': 'scandium', 'ti': 'titanium', 'v': 'vanadium', 'cr': 'chromium', 'mn': 'manganese',
    'fe': 'iron', 'co': 'cobalt', 'ni': 'nickel', 'cu': 'copper', 'zn': 'zinc',
    'ga': 'gallium', 'ge': 'germanium', 'as': 'arsenic', 'se': 'selenium', 'br': 'bromine',
    'kr': 'krypton', 'rb': 'rubidium', 'sr': 'strontium', 'y': 'yttrium', 'zr': 'zirconium',
    'nb': 'niobium', 'mo': 'molybdenum', 'tc': 'technetium', 'ru': 'ruthenium', 'rh': 'rhodium',
    'pd': 'palladium', 'ag': 'silver', 'cd': 'cadmium', 'in': 'indium', 'sn': 'tin',
    'sb': 'antimony', 'te': 'tellurium', 'i': 'iodine', 'xe': 'xenon', 'cs': 'cesium', 'ba': 'barium',
    'la': 'lanthanum', 'ce': 'cerium', 'pr': 'praseodymium', 'nd': 'neodymium', 'pm': 'promethium',
    'sm': 'samarium', 'eu': 'europium', 'gd': 'gadolinium', 'tb': 'terbium', 'dy': 'dysprosium',
    'ho': 'holmium', 'er': 'erbium', 'tm': 'thulium', 'yb': 'ytterbium', 'lu': 'lutetium',
    'hf': 'hafnium', 'ta': 'tantalum', 'w': 'tungsten', 're': 'rhenium', 'os': 'osmium',
    'ir': 'iridium', 'pt': 'platinum', 'au': 'gold', 'hg': 'mercury', 'tl': 'thallium',
    'pb': 'lead', 'bi': 'bismuth', 'po': 'polonium', 'at': 'astatine', 'rn': 'radon',
    'fr': 'francium', 'ra': 'radium', 'ac': 'actinium', 'th': 'thorium', 'pa': 'protactinium',
    'u': 'uranium', 'np': 'neptunium', 'pu': 'plutonium', 'am': 'americium', 'cm': 'curium',
    'bk': 'berkelium', 'cf': 'californium', 'es': 'einsteinium', 'fm': 'fermium', 'md': 'mendelevium',
    'no': 'nobelium', 'lr': 'lawrencium', 'rf': 'rutherfordium', 'db': 'dubnium', 'sg': 'seaborgium',
    'bh': 'bohrium', 'hs': 'hassium', 'mt': 'meitnerium', 'ds': 'darmstadtium', 'rg': 'roentgenium',
    'cn': 'copernicium', 'nh': 'nihonium', 'fl': 'flerovium', 'mc': 'moscovium', 'lv': 'livermorium',
    'ts': 'tennessine', 'og': 'oganesson','h2o': 'water',
    'co2': 'carbon dioxide',
    'ch4': 'methane',   
    'nh3': 'ammonia',
    'h2o2': 'hydrogen peroxide',
    'c2h5oh': 'ethanol',
    'ch3cooh': 'acetic acid',
    'nacl': 'sodium chloride',
    'h2so4': 'sulfuric acid',
    'hno3': 'nitric acid',
'c6h12o6': 'glucose',
    'c6h8o7': 'citric acid',
    'c6h14': 'hexane',
    'c10h16n2o3s': 'penicillin',
    'c27h46o': 'cholesterol',
    'c3h8o3': 'glycerol',
    'c8h10n4o2': 'caffeine',
    'c3h6o': 'acetone',
    'c6h6': 'benzene',
    'c2h5no2': 'glycine',
    'c7h6o2': 'benzoic acid',
    'c8h11n': 'nicotine',
    'c6h5oh': 'phenol',
    'c18h22o2': 'testosterone',
    'c4h4o4': 'malic acid',
    'c12h22o11': 'sucrose',
    'c3h7no2': 'alanine',
    'c21h30o2': 'progesterone',
    'c3h6o2': 'lactic acid',
    'c5h5n': 'pyridine',
    'c4h10o': 'butanol',
    'c4h6o3': 'acetic anhydride',
    'c5h4n4o': 'uracil',
    'c2h5n3o2': 'creatine',
    'c4h6o6': 'tartaric acid',
    'c6h5cho': 'benzaldehyde',
    'c7h8o': 'phenylacetone',
    'c6h10o5': 'cellulose',
    'c8h10n4o2': 'theobromine',
    'c7h5n3o6': 'caffeic acid',
    'c9h8o4': 'aspirin',
    'c18h24o2': 'estradiol',
    'c6h12o2': 'ethyl acetate',
    'c2h6o2': 'ethylene glycol',
    'c5h10o5': 'ribose',
    'c3h4o2': 'propionic acid',
    'c3h4o': 'acrylate',
    'c2h5clo': 'chloroethane',
    'c7h6o3': 'salicylic acid',
    'c7h14o2': 'butyl acetate',
    'c3h6o2': 'formic acid',
    'c3h4o2': 'malonic acid',
    'c7h8': 'toluene',
    'c7h5no3s': 'sulfanilamide',
    'c3h4o3': 'oxalic acid',
    'c3h6n6': 'melamine',
    'c5h10o4': 'dimethyl malonate',
    'c2h2o4': 'oxalic acid',
    'c2h6os': 'dimethyl sulfoxide',
    'c10h14n2o': 'nicotinamide',
    'c7h6o4': 'salicylic acid',
    'c3h7no2': 'serine',
    'c8h10n4o2': 'theophylline',
    'c5h10o2': 'ethyl acetate',
    'c2h5no': 'nitroethane',
    'c6h14o6': 'sorbitol',
    'c6h5ch3': 'toluene',
    'c6h12n4': 'adenine',
    'c8h18': 'octane',
    'c10h12n2o': 'phenylephrine',
    'c6h8o6': 'ascorbic acid',
    'c7h8o2': 'p-cresol',
    'c4h6o4': 'fumaric acid',
    'c3h6o': 'acetone',
    'c8h10n4o2': 'trimethoprim',
    'c6h12o6': 'fructose',
    'c7h5n': 'aniline',
    'c9h9no': 'acetaminophen',
    'c5h11no2': 'lysine',
    'c10h14n2': 'pyridoxine',
    'c7h5n3o6': 'chlorogenic acid',
    'c5h12': 'pentane',
    'c5h10o': 'butyraldehyde',
    'c9h8o4': 'methyl salicylate',
    'c8h7no2': 'indole-3-acetic acid',
    'c2h4o2': 'acetic acid',
    'c7h8o3': 'vanillin',
    'c6h8o7': 'tartaric acid',
    'c5h12n2o2': 'creatine',
    'c8h10n4o2': 'caffeine',
    'c3h8o': 'propanol',
    'c8h8o3': 'vanillin',
    'c9h8o4': 'salicylic acid',
    'c8h7no3': 'indole-3-carboxylic acid',
    'c8h7n': 'pyridine',
    'c6h8o2': 'acetaminophen',
    'c6h8o2': 'benzoic acid',
    'c3h4o2': 'acrylic acid',
    'c6h12o6': 'glucose',
    'c10h12n2o': 'phenylephrine',
    }
    normalized_tokens = [element_dict.get(token, token) for token in tokens]
    return normalized_tokens


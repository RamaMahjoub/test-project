import ir_datasets
import csv
import codecs
from text_proccessing import _get_proccessed_text
from collections import defaultdict
from nltk.corpus import stopwords, words
from inverted_index import create_weighted_inverted_index
import shelve


dataset = ir_datasets.load("lotte/science/dev/forum")

# Get the path to the TSV file
tsv_path = dataset.docs_path()
items=[]
# Open the TSV file with the correct encoding
with codecs.open(tsv_path, 'r', encoding='utf-8') as tsv_file:
    # Create a CSV reader for TSV files
    reader = csv.reader(tsv_file, delimiter='\t')

    # Iterate over the rows in the TSV file
    
    for row in reader:
        # Process each row as needed
        id = row[0]
        text = row[1]
        items.append(dict(id=id,text=text))
    

cleaned_tokens=[dict(id=item["id"],tokens=_get_proccessed_text(item["text"])) for item in items[:10]]
# print(cleaned_tokens)

create_weighted_inverted_index(cleaned_tokens)

with shelve.open('db/' + "dataset_name" + '_inverted_index.db') as db:
        # Store the inverted index in the "shelve" file
        print(db['inverted_index'])

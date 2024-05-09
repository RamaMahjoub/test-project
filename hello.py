import ir_datasets
import csv
import codecs
from text_proccessing import _get_words_tokenize,_filter_tokens,_remove_punctuations,_lowercase_tokens,_lemmatize_tokens,_stem_tokens
# Load the dataset
dataset = ir_datasets.load("lotte/science/dev/forum")

# Get the path to the TSV file
tsv_path = dataset.docs_path()
items=[dict(id="0",text="ploi")]
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
    
#    print(items[:200])

for item in items[:10]:
    non_punctuation_text=_remove_punctuations(item["text"])
    print(non_punctuation_text)
    print("*****************************************************************************")
    # tokens=_get_words_tokenize(non_punctuation_text)
    # print(tokens)
    filtered_tokens=_filter_tokens(non_punctuation_text)
    lowercase_tokens=_lowercase_tokens(filtered_tokens)
    stem=_stem_tokens(lowercase_tokens)
    print(stem)
    
    print("-----------------------------------------------------------------------------------------------------------")
    

from inverted_index import get_corpus
import csv
import codecs
from crawling import expand_document_with_crawled_data
import ir_datasets

dataset_name="science"

dataset = ir_datasets.load("lotte/science/dev/forum")

# Get the path to the TSV file
tsv_path = dataset.docs_path()
crawling_data = []
output_tsv_path = r"E:\University\Fifth_year\IR\lotte\science\dev\crawling_data8.tsv"
with codecs.open(tsv_path, 'r', encoding='utf-8') as tsv_file:
    reader = csv.reader(tsv_file, delimiter='\t')
    with open(output_tsv_path, 'w', newline='', encoding='utf-8') as output:
    # Create a CSV writer object with tab delimiter
        writer = csv.writer(output, delimiter='\t')
        for row in reader:
            expanded_data = expand_document_with_crawled_data(row[1])
            print("expanded_data: " ,row[0])
            writer.writerow([row[0],expanded_data])




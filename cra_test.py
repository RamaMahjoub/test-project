from inverted_index import get_corpus
import csv
import codecs
from crowling import expand_document_with_crawled_data
import ir_datasets

dataset_name="science"
# items=get_corpus(dataset_name)

dataset = ir_datasets.load("lotte/science/dev/forum")

# Get the path to the TSV file
tsv_path = dataset.docs_path()
# items=[]
crawling_data = []
output_tsv_path = r"E:\University\Fifth_year\IR\lotte\science\dev\crawling_data8.tsv"
with codecs.open(tsv_path, 'r', encoding='utf-8') as tsv_file:
    reader = csv.reader(tsv_file, delimiter='\t')
    with open(output_tsv_path, 'w', newline='', encoding='utf-8') as output:
    # Create a CSV writer object with tab delimiter
        writer = csv.writer(output, delimiter='\t')
        # i=0
        for row in reader:
            # print(i)
            if int(row[0])>21336 and int(row[0])<134649:
                # if i<19574:
                #     print("expanded_data:: " ,row[0])
                #     writer.writerow([row[0],row[1]])
                # else:
                expanded_data = expand_document_with_crawled_data(row[1])
                print("expanded_data: " ,row[0])
                writer.writerow([row[0],expanded_data])
            # i+=1


# with open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
#     writer = csv.writer(csv_file, delimiter=',')  # Use comma for standard CSV
#     for data in crawling_data:
#         writer.writerow(data)



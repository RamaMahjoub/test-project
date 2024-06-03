import ir_datasets


def get_qrels_map(dataset_name:str,type:str):
    qrels_map = dict()
    qas_search =list(ir_datasets.load("lotte/"+dataset_name+"/dev/"+type).qrels_iter())
    for qrel in qas_search:
        # print(qrel)
        if qrel.query_id in qrels_map:
            qrels_map[qrel.query_id].append(qrel.doc_id)
        else: 
            qrels_map[qrel.query_id] = [qrel.doc_id]
    return qrels_map


def calculate_all_evaluation(dataset_name:str,type:str,queries_answers):
    result={}
    over_all_p10=0
    over_all_recall=0
    map = 0
    mrr=0.0
    qas_search = get_qrels_map(dataset_name,type)
    for id,value in list(queries_answers.items()):
        # print(f"num: {len(list(queries_answers[id]))}")
        precision_10=calculate_precision_at_10(value,qas_search[id],10)
        over_all_p10+=precision_10
        recall=calculate_recall(value,qas_search[id])
        over_all_recall+=recall
        ap=average_precision(value,qas_search[id],10)
        map+=ap
        mrr=mrr+calculate_MRR(value, qas_search[id],10)
        result[id]={
            'precision': precision_10,
            'recall': recall,
            'ap': ap,
        }
    result['overall']={
        'precision': over_all_p10/len(list(queries_answers.items())),
        'recall': over_all_recall/len(list(queries_answers.items())),
        'map': map/len(list(queries_answers.items())),
        'mrr': mrr/len(list(queries_answers.items())),
    }
    return result

def calculate_precision_at_10(top_related_docs,query_result,k=10):
    count=0
    #  الصح تبعي  /  الصح الأصلي
    for related_doc in top_related_docs[:k]:
        if related_doc[0] in query_result:
            count=count+1
    return count/min(k,len(query_result))
 
 
def calculate_recall(top_related_docs,query_result):
    count=0
    # الصح عندي / ع ع كل شي جبته انا 
    for related_doc in top_related_docs:
        if related_doc[0] in query_result:
            count = count + 1
    return count/len(query_result)     


def calculate_MRR(top_related_docs,query_result,k=10)->float:
    
    
    for i,related_doc in enumerate(top_related_docs[:k]):
        if related_doc[0] in query_result:
            return 1.0/(i+1)
    return 0.0


def average_precision(results, relevant_docs,k=10):
    # [ 1 , 3 , 4  ,6   ]
    relevant_positions = [i for i, doc in enumerate(results[:k]) if doc[0] in relevant_docs]
    if not relevant_positions:
        return 0.0
    # [(  1 ) / 2   ,  (2 / 4 )  , .... ]
    precisions = [(i + 1) / (pos + 1) for i, pos in enumerate(relevant_positions)]
    return sum(precisions) / len(relevant_positions)

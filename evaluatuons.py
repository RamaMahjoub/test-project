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
    for related_doc in top_related_docs[:k]:
        if related_doc[0] in query_result:
            count=count+1
    return count/min(k,len(query_result))
 
 
def calculate_recall(top_related_docs,query_result):
    count=0
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
    relevant_positions = [i for i, doc in enumerate(results[:k]) if doc[0] in relevant_docs]
    if not relevant_positions:
        return 0.0
    precisions = [(i + 1) / (pos + 1) for i, pos in enumerate(relevant_positions)]
    return sum(precisions) / len(relevant_positions)
    

def compute_metrics(ranked_docs, k,dataset_name,type):
    qrels=get_qrels_map(dataset_name,type)
    metrics = {}
    ap_sum = 0
    mrr_sum = 0
    p10_sum = 0
    overall_precision = 0
    overall_recall = 0
    overall_f1_score = 0
    for query_id in ranked_docs.keys():
        ranked_list = ranked_docs[query_id]
        relevant_docs = [doc_id for doc_id in qrels[query_id] ]
        if k is not None:
            ranked_list = {key: value for key, value in list(ranked_list)[:k]}
        tp = len(set(ranked_list).intersection(set(relevant_docs)))
        precision = tp / len(ranked_list) if len(ranked_list) > 0 else 0
        recall = tp / len(relevant_docs) if len(relevant_docs) > 0 else 0
        f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        overall_precision += precision
        overall_recall += recall
        overall_f1_score += f1_score
        ap = 0
        relevant_docs_seen = set()
        for i, doc_id in enumerate(ranked_list):
            if doc_id in relevant_docs and doc_id not in relevant_docs_seen:
                ap += (len(relevant_docs_seen) + 1) / (i + 1)
                relevant_docs_seen.add(doc_id)
                if len(relevant_docs_seen) == 1:
                    mrr_sum += 1 / (i + 1)
                if len(relevant_docs_seen) == len(relevant_docs):
                    break
        ap /= len(relevant_docs) if len(relevant_docs) > 0 else 1
        ap_sum += ap
        p10 = len(set(list(tuple(ranked_list))[:10]).intersection(set(relevant_docs)))
        p10_sum += p10 / 10
        metrics[query_id] = {
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'ap': ap,
            'p10': p10
        }
    overall_precision = overall_precision / len(ranked_docs)
    overall_recall = overall_recall / len(ranked_docs)
    overall_f1_score = overall_f1_score / len(ranked_docs)
    overall_ap = ap_sum / len(ranked_docs)
    overall_mrr = mrr_sum / len(ranked_docs)
    overall_p10 = p10_sum / len(ranked_docs)
    metrics['overall'] = {
        'precision': overall_precision,
        'recall': overall_recall,
        'f1_score': overall_f1_score,
        'map': overall_ap,
        'mrr': overall_mrr,
        'p10': overall_p10
    }
    # return metrics
    return metrics["overall"]



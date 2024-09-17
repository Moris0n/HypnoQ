from time import time
import json

from chains.hypnoq_chain import qna_vector_chain, eval_chain

def evaluate_relevance(question, answer):
    
    response = eval_chain.invoke({"question" : question, "llm_answer" : answer})

    try:
        json_eval = json.loads(response.content)
        return json_eval, response.response_metadata
    except json.JSONDecodeError:
        result = {"Relevance": "UNKNOWN", "Explanation": "Failed to parse evaluation"}
        return result, response.response_metadata


def rag(question):
    t0 = time()
    print('rag')
    response = qna_vector_chain.invoke({"question" : question})
    answer, data = response.content, response.response_metadata
    print('rag response')
    evaluation, rel_data = evaluate_relevance(question, answer)
    
    print('rag eval')

    t1 = time()
    took = t1 - t0

    answer_data = {
        'answer' : answer,
        'model_name': data['model_name'],
        'qna_time': data['token_usage']['total_time'], 
        'eval_time': rel_data['token_usage']['total_time'], 
        'total_time' : took,
        'relevance': evaluation.get("Relevance", "UNKNOWN"),
        'relevance_explanation': evaluation.get("Explanation", "Failed to parse evaluation"),
        'completion_tokens': data['token_usage']['completion_tokens'],
        'prompt_tokens': data['token_usage']['prompt_tokens'],
        'total_tokens': data['token_usage']['total_tokens'],
        'eval_prompt_tokens' : rel_data['token_usage']['prompt_tokens'],
        'eval_completion_tokens': rel_data['token_usage']['completion_tokens'],
        'eval_total_tokens': rel_data['token_usage']['total_tokens'],
    }

    return answer_data
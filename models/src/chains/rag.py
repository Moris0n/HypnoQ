import json
import logging
import time

from chains.hypnoq_chain import qna_vector_chain, eval_chain

# Set up logging for better error tracing
logging.basicConfig(level=logging.INFO)

def retrieve_relevance(question):
    try:
        response = qna_vector_chain.invoke({"question": question})
        answer = response.content
        data = response.response_metadata
        return answer, data
    except Exception as e:
        logging.error(f"An error occurred while retrieving relevance: {e}")
        return None, None

def evaluate_relevance(question, answer):
    try:
        response = eval_chain.invoke({"question": question, "llm_answer": answer})
        json_eval = json.loads(response.content)
        return json_eval, response.response_metadata
    except json.JSONDecodeError:
        logging.warning("Failed to parse evaluation response as JSON.")
        result = {"Relevance": "UNKNOWN", "Explanation": "Failed to parse evaluation"}
        return result, response.response_metadata
    except Exception as e:
        logging.error(f"An error occurred during relevance evaluation: {e}")
        return {"Relevance": "UNKNOWN", "Explanation": "Evaluation failed"}, None

def get_token_usage(data, key, default=0):
    return data.get('token_usage', {}).get(key, default)

def rag(question):
    start_time = time.time()

    # Retrieve answer and relevance data
    answer, data = retrieve_relevance(question)
    if not answer or not data:
        logging.error("Failed to retrieve relevance. Returning early.")
        return None

    # Evaluate the answer relevance
    evaluation, rel_data = evaluate_relevance(question, answer)
    if not evaluation or not rel_data:
        logging.error("Failed to evaluate relevance. Returning early.")
        return None

    # Measure time taken for the entire process
    total_time = time.time() - start_time

    # Construct response data using helper to handle missing keys
    answer_data = {
        'answer': answer,
        'model_name': data.get('model_name', 'unknown_model'),
        'qna_time': get_token_usage(data, 'total_time', 0.0),
        'eval_time': get_token_usage(rel_data, 'total_time', 0.0),
        'total_time': total_time,
        'relevance': evaluation.get("Relevance", "UNKNOWN"),
        'relevance_explanation': evaluation.get("Explanation", "No explanation provided"),
        'completion_tokens': get_token_usage(data, 'completion_tokens'),
        'prompt_tokens': get_token_usage(data, 'prompt_tokens'),
        'total_tokens': get_token_usage(data, 'total_tokens'),
        'eval_prompt_tokens': get_token_usage(rel_data, 'prompt_tokens'),
        'eval_completion_tokens': get_token_usage(rel_data, 'completion_tokens'),
        'eval_total_tokens': get_token_usage(rel_data, 'total_tokens'),
    }

    return answer_data

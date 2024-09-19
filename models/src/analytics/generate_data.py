import time
import random
import uuid
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from db import save_conversation, save_feedback, get_db_connection

# Set the timezone to CET (Europe/Berlin)
tz = ZoneInfo("Europe/Berlin")

# List of sample questions and answers specific to hypnotherapy
SAMPLE_QUESTIONS = [
    "What is hypnotherapy?",
    "Is hypnotherapy safe?",
    "How many sessions of hypnotherapy are required?",
    "Can hypnotherapy help with anxiety?",
    "What should I expect during a hypnotherapy session?",
]

SAMPLE_ANSWERS = [
    "Hypnotherapy is a form of therapy that uses hypnosis to help treat various conditions.",
    "Yes, hypnotherapy is considered safe when conducted by a trained professional.",
    "The number of sessions required depends on the individual and the condition being treated.",
    "Hypnotherapy can be effective in managing anxiety and promoting relaxation.",
    "During a session, the therapist will guide you into a relaxed state and work with your subconscious mind.",
]

MODELS = ["mixtral-8x7b", "openai/gpt-3.5-turbo", "fastembed"]
RELEVANCE = ["RELEVANT", "PARTLY_RELEVANT", "NON_RELEVANT"]

def generate_synthetic_data(start_time, end_time):
    current_time = start_time
    conversation_count = 0
    print(f"Starting historical data generation from {start_time} to {end_time}")
    
    while current_time < end_time:
        conversation_id = str(uuid.uuid4())
        question = random.choice(SAMPLE_QUESTIONS)
        answer = random.choice(SAMPLE_ANSWERS)
        model = random.choice(MODELS)
        relevance = random.choice(RELEVANCE)
        
        qna_time = random.uniform(0.5, 5.0)
        eval_time = random.uniform(0.1, 2.0)
        response_time = random.uniform(0.5, 5.0)
        
        prompt_tokens = random.randint(50, 200)
        completion_tokens = random.randint(50, 300)
        total_tokens = prompt_tokens + completion_tokens
        eval_prompt_tokens = random.randint(50, 150)
        eval_completion_tokens = random.randint(20, 100)
        eval_total_tokens = eval_prompt_tokens + eval_completion_tokens

        answer_data = {
            "answer": answer,
            "model_name": model,
            "qna_time" : qna_time,
            "eval_time" : eval_time,
            "total_time": response_time,
            "relevance": relevance,
            "relevance_explanation": f"This answer is {relevance.lower()} to the question.",
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "eval_prompt_tokens": eval_prompt_tokens,
            "eval_completion_tokens": eval_completion_tokens,
            "eval_total_tokens": eval_total_tokens,
        }

        save_conversation(
            conversation_id, question, answer_data, current_time
        )
        print(f"Saved conversation: ID={conversation_id}, Time={current_time}, Model={model}")

        if random.random() < 0.7:
            feedback = 1 if random.random() < 0.8 else -1
            save_feedback(conversation_id, feedback, current_time)
            print(f"Saved feedback for conversation {conversation_id}: {'Positive' if feedback > 0 else 'Negative'}")

        current_time += timedelta(minutes=random.randint(1, 15))
        conversation_count += 1
        if conversation_count % 10 == 0:
            print(f"Generated {conversation_count} conversations so far...")

    print(f"Historical data generation complete. Total conversations: {conversation_count}")

if __name__ == "__main__":
    print(f"Script started at {datetime.now(tz)}")
    end_time = datetime.now(tz)
    start_time = end_time - timedelta(hours=6)
    print(f"Generating historical data from {start_time} to {end_time}")
    generate_synthetic_data(start_time, end_time)
    print("Historical data generation complete.")

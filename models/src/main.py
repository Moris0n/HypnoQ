from data_models.models import HypnoQueryInput, HypnoQueryOutput, FeedbackInput, FeedbackOutput
from chains.rag import rag
from analytics.db import save_conversation
from utils.async_utils import async_retry
import uuid

from fastapi import FastAPI

app = FastAPI( 
    title="Hypno Q&A Chatbot",
    description="Endpoints for a hypnotherapy Q&A RAG chatbot",)

@async_retry(max_retries=10, delay=3)
async def invoke_chain_with_retry(query: str):
    """Retry the agent if a tool fails to run.

    This can help when there are intermittent connection issues
    to external APIs.
    """
    # Ensure the input is in the correct format
    print('invoke chain with retry delay 3')
    res = rag(query)
    print(res)
    return await res

@app.get("/")
async def get_status():
    return {"status": "running"}

@app.post("/hypno-bot")
async def query_hypno_rag(query: HypnoQueryInput) -> HypnoQueryOutput:
    print('hypno bot pst')
    answer_data = await invoke_chain_with_retry(query.question)

    conversation_id = str(uuid.uuid4())

    save_conversation(
        conversation_id=conversation_id,
        question=question,
        answer_data=answer_data,
    )

    query_response = await invoke_chain_with_retry(query.question)

    output_text = answer_data.get('answer', 'No answer found')
    print(f'hypno bot ans {output_text}')
    return HypnoQueryOutput(input=query.question, output=output_text)

@app.post("/feedback")
async def provide_feedback(feedback: FeedbackInput) -> FeedbackOutput:
    if feedback.helpful:
        return FeedbackOutput(message="Thank you for your feedback!")
    else:
        return FeedbackOutput(
            message="Sorry that the answer wasn't helpful. We'll review the question.",
            original_question=feedback.question
        )

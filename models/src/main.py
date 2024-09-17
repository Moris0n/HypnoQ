from data_models.models import HypnoQueryInput, HypnoQueryOutput, FeedbackInput, FeedbackOutput
from chains.hypnoq_chain import qna_vector_chain
from utils.async_utils import async_retry

from fastapi import FastAPI

app = FastAPI( 
    title="Hypno Q&A Chatbot",
    description="Endpoints for a hypnotherapy Q&A RAG chatbot",)

@async_retry(max_retries=10, delay=1)
async def invoke_chain_with_retry(query: str):
    """Retry the agent if a tool fails to run.

    This can help when there are intermittent connection issues
    to external APIs.
    """
    # Ensure the input is in the correct format
    print(f"Print query : {query}")
    print(f"Print query quest: {query.question}")
    return await qna_vector_chain.invoke({"question": query})

@app.get("/")
async def get_status():
    return {"status": "running"}

@app.post("/hypno-bot")
async def query_hypno_rag(query: HypnoQueryInput) -> HypnoQueryOutput:
    query_response = await invoke_chain_with_retry(query.question)

    output_text = query_response.get('result', 'No answer found')

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

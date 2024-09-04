from data_models.models import HypnoQueryInput, HypnoQueryOutput
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
    return await qna_vector_chain.ainvoke({"query": query})

@app.get("/")
async def get_status():
    return {"status": "running"}

@app.post("/hypno-bot")
async def query_hypno_rag(query: HypnoQueryInput) -> HypnoQueryOutput:
    query_response = await invoke_chain_with_retry(query.question)

    return HypnoQueryOutput(input=query.question, output=query_response['result'])

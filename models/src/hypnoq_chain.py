import os

from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq 
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)

# File paths and other configurations
EMBEDDING_MODEL =  os.getenv("EMBEDDING_MODEL")
LLM_MODEL = os.getenv("LLM_MODEL")
INDEX_NAME = os.getenv("INDEX_NAME")

embed_model = FastEmbedEmbeddings(model_name=EMBEDDING_MODEL)

vector_store = FAISS.load_local(
    INDEX_NAME, embed_model, allow_dangerous_deserialization=True
)

# Initialize the Groq LLM
groq_llm = ChatGroq(
    model=LLM_MODEL,
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

qna_prompt = """Your task is to use the provided content to answer questions about hypnotherapy services offered by the hypnotherapist. 
Use the following context to provide detailed and accurate information. 
Do not create or assume information beyond what is given in the context. 
If the answer is not covered by the provided context, 
kindly encourage the client to reach out to the hypnotherapist directly via email or phone for more information.
{context}
"""

qna_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["context"], template=qna_prompt)
)

qna_human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["question"], template="{question}")
)
messages = [qna_system_prompt, qna_human_prompt]

qna_template = ChatPromptTemplate(
    input_variables=["context", "question"], messages=messages
)

retriver = vector_store.as_retriever(search_type="similarity_score_threshold", 
                                            search_kwargs={"score_threshold": .5, 
                                            "k": 5})

qna_vector_chain = RetrievalQA.from_chain_type(
    llm=groq_llm,
    chain_type="stuff",
    retriever=retriver,
)

qna_vector_chain.combine_documents_chain.llm_chain.prompt = qna_template

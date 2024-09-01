import os

from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader

# File paths and other configurations
DATA_PATH =  os.getenv("DATA_PATH")
INDEX_NAME = os.getenv("INDEX_NAME")

# Initialize the document loader
loader = DirectoryLoader(DATA_PATH, glob="**/*.md", loader_cls=TextLoader)

# Load all markdown files
documents = loader.load()

# Define headers to split on with labels (e.g., `#`, `##`, `###`)
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
    ("####", "Header 4")
]

# Initialize the MarkdownHeaderTextSplitter
splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

# Split the documents into smaller chunks and combine headers with their respective text
split_documents = []
for document in documents:
    split_texts = splitter.split_text(document.page_content)
    for text_chunk in split_texts:
        question = (text_chunk.metadata.get('Header 4', ''))
        answer = (text_chunk.page_content)
        text_chunk.page_content=f"{question}\n{answer}"
        
    split_documents+=split_texts


# Initialize the embedding model (using OpenAI here, you can use others like HuggingFace)
embed_model = FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5")

# Create a FAISS vector store
vector_store = FAISS.from_documents(split_documents, embed_model)

# Optionally, save the vector store for later use
vector_store.save_local(INDEX_NAME)

import dotenv

from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader

dotenv.load_dotenv(encoding='utf-8')

# File paths and other configurations
DATA_PATH = 'data'
INDEX_NAME = 'hypnoq_index'

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
        # Combine header with the text
        header_content = " ".join([text_chunk["metadata"][label] for label in headers_to_split_on if label in text_chunk["metadata"]])
        combined_text = f"{header_content}\n{text_chunk['content']}"
        split_documents+=(Document(page_content=combined_text))


# Initialize the embedding model (using OpenAI here, you can use others like HuggingFace)
embed_model = FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5")

# Create a FAISS vector store
vector_store = FAISS.from_documents(split_documents, embed_model)

# Optionally, save the vector store for later use
vector_store.save_local(INDEX_NAME)

# You can load it back later with
# vector_store = FAISS.load_local("faiss_vector_store", embedding_model)
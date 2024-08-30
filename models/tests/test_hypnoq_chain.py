import unittest
from unittest.mock import patch, MagicMock
import os
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.chains import RetrievalQA
from langchain.retrievers import MergerRetriever
from langchain.schema import Document

class TestHypnotherapyQA(unittest.TestCase):

    @patch.dict(os.environ, {
        "EMBEDDING_MODEL": "BAAI/bge-base-en-v1.5",  # Use a valid model name
        "LLM_MODEL": "mock_llm_model",
        "INDEX_NAME": "mock_index_name"
    })
    @patch("langchain_community.vectorstores.FAISS.load_local")
    @patch("langchain_groq.ChatGroq")
    @patch("langchain_community.embeddings.fastembed.FastEmbedEmbeddings")
    def test_chain_creation(self, mock_embed_class, mock_groq_class, mock_faiss_load_local):
        # Arrange: Create mock instances
        mock_embed_instance = MagicMock()
        mock_embed_class.return_value = mock_embed_instance
        
        mock_vector_store = MagicMock()
        mock_faiss_load_local.return_value = mock_vector_store

        # Use MergerRetriever as a concrete retriever
        mock_retriever = MagicMock(spec=MergerRetriever)
        mock_retriever.return_value._get_relevant_documents.return_value = [Document(page_content="Mock content")]

        mock_groq_instance = MagicMock()
        mock_groq_class.return_value = mock_groq_instance
        
        # Act: Execute the main part of the code
        embed_model = FastEmbedEmbeddings(model_name=os.getenv("EMBEDDING_MODEL"))
        groq_llm = ChatGroq(model=os.getenv("LLM_MODEL"))

        # Load vector store and create the QA chain
        new_vector_store = FAISS.load_local(os.getenv("INDEX_NAME"), embed_model)

        qa_chain = RetrievalQA.from_chain_type(
            llm=groq_llm,
            chain_type="stuff",
            retriever=mock_retriever  # Use the mock retriever
        )
        
        # Assert: Check that components were created and called
        mock_embed_class.assert_called_once_with(model_name="BAAI/bge-base-en-v1.5")
        mock_faiss_load_local.assert_called_once_with("mock_index_name", mock_embed_instance)
        mock_groq_class.assert_called_once_with(model="mock_llm_model")
        self.assertIsInstance(qa_chain, RetrievalQA)

if __name__ == "__main__":
    unittest.main()

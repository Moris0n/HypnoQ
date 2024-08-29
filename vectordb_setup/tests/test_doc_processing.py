import unittest
import os
import dotenv
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader

class TestDocumentProcessing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        dotenv.load_dotenv(encoding='utf-8')
        cls.DATA_PATH = 'data'
        cls.INDEX_NAME = 'hypnoq_index'
        cls.loader = DirectoryLoader(cls.DATA_PATH, glob="**/*.md", loader_cls=TextLoader)
        cls.documents = cls.loader.load()
        cls.headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
            ("####", "Header 4")
        ]
        cls.splitter = MarkdownHeaderTextSplitter(headers_to_split_on=cls.headers_to_split_on)
        cls.embed_model = FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5")

    def test_load_documents(self):
        self.assertGreater(len(self.documents), 0, "No documents loaded")

    def test_split_documents(self):
        split_documents = []
        for document in self.documents:
            split_texts = self.splitter.split_text(document.page_content)
            split_documents += split_texts
        self.assertGreater(len(split_documents), 0, "No documents split")
    
    def test_create_vector_store(self):
        split_documents = []
        for document in self.documents:
            split_texts = self.splitter.split_text(document.page_content)
            split_documents += split_texts
        vector_store = FAISS.from_documents(split_documents, self.embed_model)
        self.assertIsNotNone(vector_store, "Vector store creation failed")
        vector_store.save_local(self.INDEX_NAME)
        self.assertTrue(os.path.exists(self.INDEX_NAME), "Vector store not saved")

if __name__ == '__main__':
    unittest.main()

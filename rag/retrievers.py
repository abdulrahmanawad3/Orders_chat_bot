from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from states import States
from langchain_community.document_loaders import CSVLoader
import os

def load_data():
    loader=CSVLoader("data/menu.csv")
    States.data=loader.load()

persist_dir = os.path.expanduser("~/.cache/chroma_db")

def load_retrievers():
    if not States.data_loaded:
        load_data()

    States.vectorstore = Chroma.from_documents(
        States.data,
        embedding=States.embedding_model,
        persist_directory=persist_dir,
        collection_metadata={"hnsw:space": "cosine"}
    )

    States.vec_retriever = States.vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 10,
            "score_threshold": 0.4
        }
    )

    States.bm25=BM25Retriever.from_documents(States.data)
    States.bm25.k=5

    States.retrievers_loaded = True
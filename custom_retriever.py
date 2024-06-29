from langchain.schema import Document
from langchain.vectorstores import Qdrant
from google.generativeai import embed_content
from typing import List

class QdrantRetriever:
    def __init__(self, vectorstore: Qdrant):
        self.vectorstore = vectorstore

    def get_relevant_documents(self, query: str) -> List[Document]:
        query_embedding = embed_content(
            model="models/embedding-001",
            content=query,
            task_type="retrieval_query",
        )["embedding"]
        search_results = self.vectorstore.similarity_search_by_vector(query_embedding, k=3)
        documents = [Document(page_content=result['payload']['text']) for result in search_results]
        return documents

    async def aget_relevant_documents(self, query: str) -> List[Document]:
        return self.get_relevant_documents(query)

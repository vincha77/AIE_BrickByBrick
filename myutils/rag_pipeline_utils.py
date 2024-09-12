"""
rag_pipeline_utils.py

This python script implements various classes useful for a RAG pipeline.

Currently I have implemented:

   Text splitting
      SimpleTextSplitter: uses RecursiveTextSplitter
      SemanticTextSplitter: uses SemanticChunker (different threshold types can be used)

   VectorStore
      currently only sets up Qdrant vector store in memory
   
   AdvancedRetriever
      simple retriever is a special case - 
      advanced retriever - currently implemented MultiQueryRetriever

"""

from operator import itemgetter

from langchain_core.runnables import RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from langchain.retrievers.multi_query import MultiQueryRetriever

from datasets import Dataset

from ragas import evaluate


class SimpleTextSplitter:
    def __init__(self, 
                 chunk_size, 
                 chunk_overlap, 
                 documents):
       self.chunk_size = chunk_size
       self.chunk_overlap = chunk_overlap
       self.documents = documents
       return
    
    def split_text(self):
       text_splitter = RecursiveCharacterTextSplitter(
          chunk_size=self.chunk_size,
          chunk_overlap=self.chunk_overlap
       )
       all_splits = text_splitter.split_documents(self.documents)
       return all_splits


class SemanticTextSplitter:
    def __init__(self, 
                 llm_embeddings=OpenAIEmbeddings(), 
                 threshold_type="interquartile", 
                 documents=None):
       self.llm_embeddings = llm_embeddings
       self.threshold_type = threshold_type
       self.documents = documents
       return
    
    def split_text(self):
       text_splitter = SemanticChunker(
          embeddings=self.llm_embeddings,
          breakpoint_threshold_type="interquartile"
       )

       print(f'loaded {len(self.documents)} to be split ')
       all_splits = text_splitter.split_documents(self.documents)
       print(f'returning docs split into {len(all_splits)} chunks ')
       return all_splits


class VectorStore:
    def __init__(self,
                 location,
                 name,
                 documents,
                 size,
                 embedding=OpenAIEmbeddings()):
       self.location = location
       self.name = name
       self.size = size
       self.documents = documents
       self.embedding = embedding

       self.qdrant_client = QdrantClient(self.location)
       self.qdrant_client.create_collection(
          collection_name=self.name,
          vectors_config=VectorParams(size=self.size, distance=Distance.COSINE),
       )
       return
    
    def set_up_vectorstore(self):
       self.qdrant_vector_store = QdrantVectorStore(
          client=self.qdrant_client,
          collection_name=self.name,
          embedding=self.embedding
       )

       self.qdrant_vector_store.add_documents(self.documents)
       return self


class AdvancedRetriever:
    def __init__(self, 
                 vectorstore):
        self.vectorstore = vectorstore
        return
        
    def set_up_simple_retriever(self):
        simple_retriever = self.vectorstore.as_retriever()
        return simple_retriever
    
    def set_up_multi_query_retriever(self, llm):
        retriever = self.set_up_simple_retriever()
        advanced_retriever = MultiQueryRetriever.from_llm(
            retriever=retriever, llm=llm
        )
        return advanced_retriever


def run_and_eval_rag_pipeline(location, collection_name, embed_dim, text_splits, embeddings,
                              prompt, qa_llm, metrics, test_df):
    """
    Helper function that runs and evaluates different rag pipelines
        based on different text_splits presented to the pipeline
    """
    # vector store
    vs = VectorStore(location=location, 
                     name=collection_name, 
                     documents=text_splits,
                     size=embed_dim, 
                     embedding=embeddings)

    qdvs = vs.set_up_vectorstore().qdrant_vector_store

    # retriever
    retriever = AdvancedRetriever(vectorstore=qdvs).set_up_simple_retriever()

    # q&a chain using LCEL
    retrieval_chain = (
        {"context": itemgetter("question") | retriever, "question": itemgetter("question")}
        | RunnablePassthrough.assign(context=itemgetter("context"))
        | {"response": prompt | qa_llm, "context": itemgetter("context")}
    )

    # get questions, and ground-truth
    test_questions = test_df["question"].values.tolist()
    test_groundtruths = test_df["ground_truth"].values.tolist()


    # run RAG pipeline
    answers = []
    contexts = []

    for question in test_questions:
        response = retrieval_chain.invoke({"question" : question})
        answers.append(response["response"].content)
        contexts.append([context.page_content for context in response["context"]])

    # Save RAG pipeline results to HF Dataset object
    response_dataset = Dataset.from_dict({
        "question" : test_questions,
        "answer" : answers,
        "contexts" : contexts,
        "ground_truth" : test_groundtruths
    })

    # Run RAGAS Evaluation - using metrics
    results = evaluate(response_dataset, metrics)

    # save results to df
    results_df = results.to_pandas()

    return results, results_df

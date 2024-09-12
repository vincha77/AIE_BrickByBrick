# My Utilities

This folder contains a number of helper functions.

[textloader.py] loads plain text files.  There's a simple loader as well as one that returns text files in a format compatible with LangChain Documents.

[pdfloader.py] uses different pdf loader modules to load pdf documents.  Currently, the classes here are simple pdf loaders and don't do a good job of parsing pdfs with tables and figures.  Forthcoming plans to add pdf loaders using LlamaParse and Unstructured modules that do a much better job with tables.

[rag_pipeline_utils.py] collects a number of helper classes to streamline a rag pipeline.  These include Text Splitting (simple as well as semantic-based), VectorStore (currently only Qdrant), Retriever as well as a helper function to run a rag eval pipeline with RAGAS.

[ragas_pipeline.py] collects classes needed to set up RAGAS and geenrate a set of questions, contexts as well as ground-truth responses.

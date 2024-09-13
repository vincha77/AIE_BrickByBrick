# RAG Evaluation

RAGAS uses an interesting framework to generate a range of questions ranging from `simple` to `multi-context` and `reasoning`.  It does this via an evolutionary approach in which a seed question is augmented via a process of evolution into a question that requires multiple contexts or reasoning.

## An exploration of RAGAS synthetically-generated questions
I thought it might be interesting to experiment with a recent text corpus - a transcript of the presidential debate between Kamala Harris and Donaly Trump that was held on September 10, 2024.  My main interest is in getting a qualitative idea of the kinds of questions that RAGAS can generate, especially in terms of multi-context and reasoning.

This [notebook](use_RAGAS_to_generate_interesting_questions.ipynb) has the code to generate RAGAS-based Question/Ground-Truth pairs as well as a comparison of two RAG pipelines that are set up to answer these questions.  The first pipeline uses simple character text splitting to chunk the text and the second uses semantic chunking to form the chunks.  The notebook has a few summary observations at the end.

Raw transcript of the debate can be found [here](data/2024_first_presidential_candidate_debate_KamalaHarris_DonaldTrump_10sep2024.txt)

Full RAGAS set of questions, contexts and responses can be found [here](data/testset_from_ragas_run.csv)

For convenience, I divided up the questions into `simple`, `multi_context` and `reasoning` and these can also be found in the [data](data) folder.

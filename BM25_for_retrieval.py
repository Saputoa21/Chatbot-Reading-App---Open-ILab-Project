from rank_bm25 import BM25Okapi
from retrieval_with_inverted_indices import indices_dict, tokenize_query, punctuation, stop_words, new_signs
from pathlib import Path
import pandas as pd


#code from the website to see how it works
# The only requirements is that the class receives a list of lists of strings, which are the document tokens.
corpus = [
    "Hello there good man!",
    "It is quite windy in London",
    "How is the weather today?",
    "How is the weather today in London?",
    "Is it windy today?",
]
tokenized_corpus = [doc.split(" ") for doc in corpus]
bm25 = BM25Okapi(tokenized_corpus)
print(bm25)

#Good to note that we also need to tokenize our query, 
#and apply the same preprocessing steps we did to the documents in order to have an apples-to-apples comparison
query = "windy London"
tokenized_query = query.split(" ")
doc_scores = bm25.get_scores(tokenized_query)
print(doc_scores)


#Instead of getting the document scores, you can also just retrieve the best documents with
relevant_docs = bm25.get_top_n(tokenized_query, corpus, n=2)
print(relevant_docs)



#Implementation for my indices
input_dir = Path("Data\splitted_dataframes_with_dif_numbers_tokenized")
csv_files = sorted(input_dir.glob("*.csv"))

tokenized_docs = []
doc_ids = []
original_texts = []

tokenixed_scv_df = pd.read_csv(csv_files[0])
for _, row in tokenixed_scv_df.iterrows():
        try:
            tokens = eval(row["tokenized"])  # Convert stringified list back to list
        except:
            continue  # skip bad rows
        doc_id = (f"Book {row['book_id']} with the title '{row['book_title']}', Chapter {row['chapter_id']}, Paragraph {row['paragraph_id']}")
        text = row["paragraph_text"]
        tokenized_docs.append(tokens)
        doc_ids.append(doc_id)
        original_texts.append(text)

# Build BM25 index
bm25 = BM25Okapi(tokenized_docs)

query = "Who is actually 'the man in the brown suit'?"
tokenized_query = tokenize_query(query, stop_words, punctuation, lemmatisation=False)

scores = bm25.get_scores(tokenized_query)

top_docs = bm25.get_top_n(tokenized_query, list(zip(doc_ids, original_texts)), n=5)

for rank, (doc_id, text) in enumerate(top_docs, 1):
    print(f"\nRank {rank}")
    print(f"Doc ID: {doc_id}")
    print(text)
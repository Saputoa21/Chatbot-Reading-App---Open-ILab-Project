import nltk
import string
from nltk.corpus import stopwords
from pathlib import Path
import pandas as pd

import spacy
nlp = spacy.load("en_core_web_sm")
print(spacy.info())  # Lists installed models

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
punctuation = set(string.punctuation)
new_signs = ['“', '‘', '’', '”', '—']  #specific signs that are not processed with just a punctuation list

print(stop_words)
print(punctuation)
print(type(punctuation))
print(len(punctuation))

# functions for tokenizing the dataframes
def tokenize_book(book, stop_words, punctuation, lemmatisation=False):
    clean_book_tokens = []
    processed_book = nlp(book)
    for token in processed_book:
        if token.text in punctuation or token.text in stop_words or token.text in new_signs:
            continue
        if lemmatisation:
            clean_book_tokens.append(token.lemma_)
        else:
            clean_book_tokens.append(token.text)
    return clean_book_tokens


# #preprocessing all books without lemmatisation
input_dir = Path("Data\splitted_dataframes_with_dif_numbers")
output_dir = Path("Data\splitted_dataframes_with_dif_numbers_tokenized")
output_dir.mkdir(exist_ok=True)

csv_files = sorted(input_dir.glob("*.csv"), key=lambda f: f.stat().st_mtime, reverse=True)[:3]

for file in csv_files:
    splitted_book = pd.read_csv(file)
    if "paragraph_text" not in splitted_book.columns:
        print(f"Skipping {file.name}, missing 'paragraph_text'")
        continue

    splitted_book["tokenized"] = splitted_book["paragraph_text"].astype(str).apply(
        lambda text: tokenize_book(text, stop_words, punctuation)
    )

    output_path = output_dir / f"tokenized_{file.name}"
    splitted_book.to_csv(output_path, index=False)
    print(f"Saved: {output_path}")


# preprocessing all books with lemmatisation
input_dir = Path("Data\splitted_dataframes_with_dif_numbers")
output_dir = Path("Data\splitted_dataframes_with_dif_numbers_tokenized_lemmatised")
output_dir.mkdir(exist_ok=True)

csv_files = sorted(input_dir.glob("*.csv"))

for file in csv_files:
    splitted_book = pd.read_csv(file)
    if "paragraph_text" not in splitted_book.columns:
        print(f"Skipping {file.name}, missing 'paragraph_text'")
        continue

    splitted_book["tokenized"] = splitted_book["paragraph_text"].astype(str).apply(
        lambda text: tokenize_book(text, stop_words, punctuation, lemmatisation = True)
    )

    output_path = output_dir / f"tokenized_lemmatised_{file.name}"
    splitted_book.to_csv(output_path, index=False)
    print(f"Saved: {output_path}")
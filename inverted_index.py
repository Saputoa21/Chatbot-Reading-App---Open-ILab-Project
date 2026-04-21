import pandas as pd
from pathlib import Path
from collections import defaultdict
import ast # pandas automatically converts the lists to strings in the CSV file so I need to handle lists like "["a", "b", "c"]}"
import pickle 

#storing inverted index in a pickle file
def save_index_as_pickle(index, output_dir, filename):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    full_path = output_path / filename
    with open(full_path, 'wb') as f: #binary write mode ('wb')
        pickle.dump(index, f) #serializing the index to the file
        print(f"Pickle saved: {full_path}")

# Create a list where each element is the 'paragraph_text' from each row
def build_inverted_index_from_tokenized_csv(csv_file):
    all_tokens = []
    all_metadata = []

    splitted_tokenised_books_df = pd.read_csv(file)
    for _, row in splitted_tokenised_books_df.iterrows():
        tokens = ast.literal_eval(row['tokenized'])  # handles wrong list masked as strings
        all_tokens.append(tokens)
        all_metadata.append({
            'book_title': row['book_title'],
            'book_id': row['book_id'],
            'chapter_id': row['chapter_id'],
            'paragraph_id': row['paragraph_id']
        })

    terms = set()
    for tokens in all_tokens:
        terms.update(tokens)
    terms = list(terms)

    inverted_index = {}

    for term in terms:
        document_ids = []
        for i, tokens in enumerate(all_tokens):
            if term in tokens:
                meta = all_metadata[i]
                doc_id = f"Book {meta['book_id']} with the title '{meta['book_title']}', Chapter {meta['chapter_id']}, Paragraph {meta['paragraph_id']}"
                document_ids.append(doc_id)
        inverted_index[term] = list(set(document_ids))

    return inverted_index

#store indices in the folder 
#lemmatised
input_dir = Path("Data/splitted_dataframes_with_dif_numbers_tokenized_lemmatised")
output_dir = Path("agatha_christie_information_retrieval_project\Index\Inverted indices")
output_dir.mkdir(parents=True, exist_ok=True)

csv_files = sorted(input_dir.glob("*.csv"))

for file in csv_files:
    inverted_index = build_inverted_index_from_tokenized_csv(file) 
    paragraph_tag = "_".join(file.stem.split("_")[-2:]) #reusing the step makes the file too long and can not be commited anymore
    pickle_filename = f"inverted_index_lemmatized_{paragraph_tag}.pkl"
    save_index_as_pickle(inverted_index, output_dir, pickle_filename)

# just tokenised
input_dir_2 = Path(r"Data\splitted_dataframes_with_dif_numbers_tokenized")
csv_files_2 = sorted(input_dir_2.glob("*.csv"))

for file in csv_files_2:
    inverted_index = build_inverted_index_from_tokenized_csv(file) 
    paragraph_tag = "_".join(file.stem.split("_")[-2:])
    pickle_filename = f"inverted_index_tokenized_{paragraph_tag}.pkl"
    save_index_as_pickle(inverted_index, output_dir, pickle_filename)
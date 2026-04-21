import zipfile
import pandas as pd
from pathlib import Path

# define paths using Path objects
zip_path = Path("Data\Agatha_Christie_Corpus.zip")
extract_path = Path("Data\Agatha_Christie_Corpus_txt")

extract_path.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

# reading one book 
file_to_read_path = extract_path / "Poirot Investigates_pg61262.txt"

with open(file_to_read_path, "r", encoding="utf-8") as file:
    content = file.read()
    print(content[:1000])


# get sorted list of filenames
filenames = sorted([f.name for f in extract_path.iterdir() if f.is_file()])
print("\nExtracted Files:")
for i, filename in enumerate(filenames):
    print(f"- {filename}")

texts = []
filenames_sorted = []
# iterate through the files in the extracted directory
for file_path in extract_path.iterdir():
    # Check if it's a file and ends with .txt
    if file_path.is_file() and file_path.suffix == ".txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            filenames_sorted.append(file_path.name) # Use .name to get just the filename
            texts.append(file.read())

print(f"Successfully loaded {len(texts)} text files.")

# create a DataFrame
agatha_chrisite_books_corpus_df = pd.DataFrame({"book_title": filenames, "content": texts})

agatha_chrisite_books_corpus_df.insert(0, 'book_id', range(0, len(agatha_chrisite_books_corpus_df)))

print(agatha_chrisite_books_corpus_df) #print the dataframe

# clean book title by removing the "_pgXXXXX.txt" part
agatha_chrisite_books_corpus_df["book_title"] = agatha_chrisite_books_corpus_df["book_title"].str.replace(r"_pg\d+\.txt$", "", regex=True)

print(agatha_chrisite_books_corpus_df)

print(agatha_chrisite_books_corpus_df['content'][0][:3000]) #printing the first book content
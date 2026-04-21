import pandas as pd
from pathlib import Path

from preprocessing_functions import delete_metadata
from preprocessing_functions import find_chapters
from preprocessing_functions import find_main_book_content
from preprocessing_functions import extract_chapters_and_paragraphs
from preprocessing_functions import chapter_regex

from preprocessing_functions import save_dataframe_to_csv

from creating_book_dataframe_from_zip import agatha_chrisite_books_corpus_df


# function to create splitted dataframe for index
def splitting_books_for_index(df, book_ids, chapter_regex, paragraph_num):
    """
    Process books from the given DataFrame by extracting chapters and paragraphs.
    Concatenates all processed book data into a single DataFrame and
    optionally saves it to a specified folder in both CSV and Excel formats.

    Parameters:
        df (pd.DataFrame): The DataFrame containing 'book_id', 'book_title', 'content'.
        book_ids (list): List of integer book IDs to process.
        chapter_regex (str): Regex pattern to identify chapters.
        paragraph_num (int): Number of paragraphs to extract per chapter.

    Returns:
        pd.DataFrame: Concatenated DataFrame of all processed book data.
    """
    all_books_df = []

    for i in book_ids:
        try:
            # Fetch book data
            book_text = df.iloc[i]["content"]
            book_title = df.iloc[i]["book_title"]
            book_id = int(df.iloc[i]["book_id"])

            # Remove metadata
            book_wo_metadata = delete_metadata(book_text)

            # Chapter list
            chapter_list = find_chapters(book_wo_metadata, chapter_regex)

            # Extract main content
            book_main_content = find_main_book_content(book_wo_metadata, chapter_list)

            # Debug output
            print(f"Processing '{book_title}' (ID {book_id}). Found {len(chapter_list)} chapters.")

            # Split into chapters and paragraphs
            book_df = extract_chapters_and_paragraphs(
                book_main_content, chapter_list, book_id, book_title, paragraph_num)

            all_books_df.append(book_df)

        except Exception as e:
            print(f"[ERROR] Book ID {df.iloc[i]['book_id']} - {df.iloc[i]['book_title']}: {e}")

    # Concatenate all individual book DataFrames into one large DataFrame AFTER the loop
    final_combined_df = pd.concat(all_books_df, ignore_index=True)
    print(f"\nSuccessfully processed and combined data for {len(book_ids)} books.")
    print(f"Total rows in combined DataFrame: {len(final_combined_df)}")

    return final_combined_df


normal_book_ids = [0, 2, 3, 5, 6, 7, 8, 12]  #results from the experiments in colab, there are the books which ger processed with created funtion in a right way
"""
 book_id                       book_title                                            content
0         0              Poirot Investigates  The Project Gutenberg eBook of Poirot Investi...
1         1                     The Big Four  The Project Gutenberg eBook of The Big Four\n...
2         2          The Hunter's Lodge Case  The Project Gutenberg eBook of The Hunter's L...
3         3                 The Missing Will  The Project Gutenberg eBook of The Man in the...
4         4      The Murder of Roger Ackroyd  The Project Gutenberg eBook of The Missing Wi...
5         5          The Murder on the Links  The Project Gutenberg eBook of The murder of ...
6         6  The Mysterious Affair at Styles  The Project Gutenberg eBook of The Murder on ...
7         7    The Mystery of the Blue Train  The Project Gutenberg eBook of The Mysterious...
8         8      The Plymouth Express Affair  The Project Gutenberg eBook of The mystery of...
9         9             The Secret Adversary  The Project Gutenberg eBook of The Plymouth E...
10       10           The Secret of Chimneys  The Project Gutenberg eBook of The Secret Adv...
11       11          The Seven Dials Mystery  The Project Gutenberg eBook of The Secret of ...
12       12        The man in the Brown Suit  The Project Gutenberg eBook of The Seven Dial...
"""

paragraph_values = [10, 15] #values of splitting paragraphs to test
combined_base_filename = "Agatha_Christie_Corpus_Combined_Index"
output_folder = "Data\splitted_dataframes_with_dif_numbers"
csv_filename = f"{combined_base_filename}.csv"

# # the case for one number for splitting
# paragaph_num = 5
# final_combined_df = splitting_books_for_index(df=agatha_chrisite_books_corpus_df, 
#                           book_ids=normal_book_ids,
#                           chapter_regex=chapter_regex, 
#                           paragraph_num=paragraph_num)

# # save to CSV
# csv_filename = f"{combined_base_filename}.csv"
# save_dataframe_to_csv(final_combined_df, output_folder, csv_filename)

# Ensure the output directory exists
output_folder_path = Path(output_folder)
output_folder_path.mkdir(parents=True, exist_ok=True)
print(f"Output files will be saved to: {output_folder_path}")

for num in paragraph_values:
    print(f"\n--- Processing with paragraph_num = {num} ---")

    # 1. Process the books to get the combined DataFrame
    final_combined_df = splitting_books_for_index(
        df=agatha_chrisite_books_corpus_df,
        book_ids=normal_book_ids,
        chapter_regex=chapter_regex,
        paragraph_num=num # Use the current 'num' from the loop
    )

    # 2. Define unique filenames based on the current 'num'
    # For CSV
    csv_filename = f"Agatha_Christie_Corpus_Combined_Paragraphs_{num}.csv"
    save_dataframe_to_csv(
        df=final_combined_df,
        output_dir=output_folder_path, # Use the Path object here
        filename=csv_filename
    )

print("\nAll processing and saving complete!")
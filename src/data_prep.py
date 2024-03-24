import csv
import os
from sefaria_api import get_tanakh_books, get_num_of_chapters, get_psukim, get_commentaries, clean_text
from multiprocessing import Process, current_process
from constants import DATA_DIR, FORMAT, COLS, COMBINED
import pandas as pd

def get_book_title_csv(book: str) -> str:
    """
    Returns the CSV file name for a given book.

    Args:
        book (str): The name of the book.

    Returns:
        str: The CSV file name for the given book.
    """
    path = os.path.join(DATA_DIR, book)
    return f'{path}.csv'


def get_book_title_txt(book: str) -> str:
    """
    Returns the title of the book with the '.txt' extension.

    Args:
        book (str): The name of the book.

    Returns:
        str: The title of the book with the '.txt' extension.
    """
    path = os.path.join(DATA_DIR, book)
    return f'{path}.txt'


def write_perushim_to_csv(pasuk: str, perushim: list, writer: csv.writer) -> None:
    """
    Writes the perushim (commentaries) for a given pasuk (verse) to a CSV file.

    Args:
        pasuk (str): The pasuk (verse) to write perushim for.
        perushim (list): List of perushim (commentaries) for the pasuk.
        writer (csv.writer): CSV writer object to write the data.

    Returns:
        None
    """
    for perush in perushim:
        commentar = clean_text(perush[0])
        perush_clr = clean_text(perush[1])
        pasuk_clr = clean_text(pasuk)
        writer.writerow([pasuk_clr, commentar, perush_clr])


def create_book_csv(book: str) -> None:
    """
    Create a CSV file for the given book.

    Args:
        book (str): The name of the book.

    Returns:
        None
    """
    columns = COLS
    if os.path.exists(get_book_title_csv(book)):
        return
    with open(get_book_title_csv(book), 'w', newline='', encoding=FORMAT) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        for chapter_idx in range(1, get_num_of_chapters(book) + 1):
            pasukim = get_psukim(book, chapter_idx)
            for pasuk_idx, pasuk in enumerate(pasukim):
                perushim = get_commentaries(book, chapter_idx, pasuk_idx + 1)
                write_perushim_to_csv(pasuk, perushim, writer)


def create_book_txt(book: str):
    """
    Create a text file for the given book (using the csv).

    Args:
        book (str): The name of the book.

    Returns:
        None
    """
    csvfile = open(get_book_title_csv(book), 'r', newline='', encoding=FORMAT)
    reader = csv.reader(csvfile)
    next(reader)  # skip the header
    with open(get_book_title_txt(book), 'w', encoding=FORMAT) as txtfile:
        pasuk_prev = ""
        for row in reader:
            pasuk, commentar, perush = row
            if pasuk != pasuk_prev:
                print(f'\nפסוק: {pasuk}', file=txtfile)

            print(f'# {commentar}', file=txtfile)
            print(f'{perush}', file=txtfile)
            pasuk_prev = pasuk
    
    csvfile.close()



def create_csv_for_each_book(books: list) -> None:
    """
    Create a CSV file for each book in the list.

    Args:
        books (list): List of books to create CSV files for.

    Returns:
        None
    """
    for book in books:
        create_book_csv(book)


def create_all_books_csv() -> None:
    """
    Create text files for all books.

    Returns:
        None
    """
    # return if the combined file already exists
    if os.path.exists(COMBINED):
        return
        
    books = get_tanakh_books()
    cpu_count = os.cpu_count() - 1
    print(f"Get CSVs using {cpu_count} Processes")
    procs = []
    books_per_core = len(books) // cpu_count
    for i in range(cpu_count):
        start = i * books_per_core
        end = start + books_per_core
        if i == cpu_count - 1:
            end = len(books)
        books_subset = books[start:end]
        p = Process(target=create_csv_for_each_book, args=(books_subset,))
        procs.append(p)
        p.start()
    
    for p in procs:
        p.join()
    
    # combine the CSV files into one combined csv file
    with open(COMBINED, 'w', newline='', encoding=FORMAT) as combined_csv:
        writer = csv.writer(combined_csv)
        writer.writerow(COLS)
        for book in books:
            with open(get_book_title_csv(book), 'r', newline='', encoding=FORMAT) as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # skip the header
                for row in reader:
                    writer.writerow(row)


def get_raw_data() -> None:
    """
    Get the raw data for all the books.

    Returns:
        None
    """
    raw_data = pd.read_csv(COMBINED)
    return raw_data

def prepare_data(raw_data: pd.DataFrame) -> pd.DataFrame:
    # remove the "Mefaresh" column
    raw_data.drop(columns=["Mefaresh"], inplace=True)
    # remove rows with empty values
    raw_data.dropna(inplace=True)
    # renaming the columns for mT5
    raw_data.columns = ['input_text', 'target_text']

    # add "summarize: " to the target_text
    return raw_data


def get_raw_data(path) -> None:
    """
    Get the raw data for all the books.

    Returns:
        None
    """
    raw_data = pd.read_csv(path)
    return raw_data

def prepare_data(raw_data: pd.DataFrame) -> pd.DataFrame:
    # remove the "Mefaresh" column
    raw_data.drop(columns=["Mefaresh"], inplace=True)
    # remove rows with empty values
    raw_data.dropna(inplace=True)
    # renaming the columns for mT5
    raw_data.columns = ['input_text', 'target_text']
    return raw_data


if __name__ == '__main__': 
    create_all_books_csv()
    df = get_raw_data()
    df = prepare_data(df)

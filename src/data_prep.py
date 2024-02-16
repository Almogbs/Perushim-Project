import csv
import os
from sefaria_api import get_tanakh_books, get_num_of_chapters, get_psukim, get_commentaries, clean_text
from constants import DATA_DIR, FORMAT

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
    columns = ["Pasuk", "Mefaresh", "Perush"]
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


if __name__ == "__main__":
    books = get_tanakh_books()
    for book in books[:1]:
        create_book_csv(book)
        #create_book_txt(book)

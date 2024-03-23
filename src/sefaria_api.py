# text utils: https://github.com/TechnionTDK/jbs-data/blob/master/raw2json/text_utils.py
from typing import List
import multiprocessing
import unicodedata
import requests
import psutil
import json
import re
import os

from constants import FORMAT

# get json from https://www.sefaria.org/api/index/
# search for an object with "category" field equal to "Tanakh"
# Within its "contents" field, search for objects with "category" field equal to "Torah", "Prophets", "Writings".
# Within each of these objects, extract the "title" field from the "contents" array.
# return a list of strings
def get_tanakh_books(he=False) -> List[str]:
    url = "https://www.sefaria.org/api/index/"
    response = requests.get(url)
    json_data = json.loads(response.text)
    titles = []
    for item in json_data:
        if item["category"] == "Tanakh":
            for content_item in item["contents"]:
                if content_item["category"] in ["Torah", "Prophets", "Writings"]:
                    for title in content_item["contents"]:
                        if he:
                            titles.append(title["heTitle"])
                        else:
                            titles.append(title["title"])
    return titles


def get_parashot(book: str, he=False) -> [List[str], List[str]]:
    # call https://www.sefaria.org/api/index/{title}
    # extract the "sections" field, and return it
    url = f"https://www.sefaria.org/api/index/{book}"
    response = requests.get(url)
    json_data = json.loads(response.text)

    # get "alts"/"Parasha"/"nodes" list. Extract from each item the "title" field
    parashot = []
    refs = []
    for item in json_data["alts"]["Parasha"]["nodes"]:
        if he:
            parashot.append(item["heTitle"])
        else:
            parashot.append(item["title"])
        refs.append(item["wholeRef"])

    return parashot, refs


def get_num_of_chapters(book: str) -> int:
    # call https://www.sefaria.org/api/index/{title}
    # extract the "schema" field, and from it the "lengths" field, and return its first element
    url = f"https://www.sefaria.org/api/index/{book}"
    response = requests.get(url)
    json_data = json.loads(response.text)
    return json_data["schema"]["lengths"][0]


def get_psukim(title: str, chapter: int) -> List[str]:
    # call https://www.sefaria.org/api/texts/{title}.{chapter}
    # extract the "he" field, and return it
    url = f"https://www.sefaria.org/api/texts/{title}.{chapter}"
    response = requests.get(url)
    json_data = json.loads(response.text)
    return json_data["he"]


def get_commentaries(book: str, chapter: int, pasuk: int) -> list:
    # call https://www.sefaria.org/api/links/{title}.{chapter}.{pasuk}
    # extract objects with "category" field equal to "Commentary"
    # extract the "heTitle" and "he" fields from each of these objects.
    # return a list of tuples (heTitle, he)
    url = f"https://www.sefaria.org/api/links/{book}.{chapter}.{pasuk}"
    process_id = os.getpid()
    cpu_affinity = psutil.Process(process_id).cpu_affinity()
    print(f"CPU={cpu_affinity}: URL={url}")
    response = requests.get(url)
    json_data = json.loads(response.text)
    commentaries = []
    for item in json_data:
        if item["category"] == "Commentary":
            book = item["collectiveTitle"]["he"]
            text = item["he"]
            # if text is a list, join it into a string
            if isinstance(text, list):
                text = " ".join(text)
            # if item has no "heTitle" or "he" fields, print a warning and continue
            if len(book) == 0 or len(text) == 0:
                # print(f"WARNING: item {item} has empty title or text")
                continue
            commentaries.append((book, text))
    return commentaries


def _strip_html(text: str) -> str:
    """
    Removes HTML tags and replaces special characters in the given text.

    Args:
        text (str): The text to be processed.

    Returns:
        str: The processed text with HTML tags removed and special characters replaced.

    """
    text = re.sub('<[^<]+?>', '', text)
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    return text


def _remove_nikud(text: str) -> str:
    """https://writing.stackexchange.com/questions/32470/how-do-i-remove-nikkud-vowel-marks-from-a-word-2016-document"""
    normalized = unicodedata.normalize('NFKD', text)
    no_nikkud = ''.join([c for c in normalized if not unicodedata.combining(c)])
    no_nikkud = no_nikkud.replace('־', ' ')  # our addition, a weird character found in texts
    no_nikkud = no_nikkud.replace('|', ' ')
    return no_nikkud


def _remove_empty_parentheses(text: str) -> str:
    """
    Removes empty parentheses from the given text.

    Args:
        text (str): The input text.

    Returns:
        str: The text with empty parentheses removed.
    """
    pattern = re.compile(r'\s*\(\s*\)\s*')
    clean_text = re.sub(pattern, ' ', text)
    
    return clean_text


def _remove_non_hebrew_letters(text: str) -> str:
    """
    Removes non-Hebrew letters from the given text.

    Args:
        text (str): The input text.

    Returns:
        str: The cleaned text with non-Hebrew letters removed.
    """
    pattern = re.compile(r'[^א-ת\s\.\,\-\(\)\'\"]')
    clean_text = re.sub(pattern, ' ', text)

    return clean_text


def _remove_footnotes(text : str) -> str:
    """
    Removes footnotes from the given text.

    Args:
        text (str): The text containing footnotes.

    Returns:
        str: The text with footnotes removed.
    """
    clean_text = re.sub(r'<sup class="footnote-marker">.*?</sup><i class="footnote">.*?</i>', '', text)

    return clean_text


def _replace_panctuation_series(text: str) -> str:
    """
    Replaces series of panctuation from the given text.
    Series of panctuation are defined as 2 or more consecutive panctuation different characters.

    Args:
        text (str): The text containing series of panctuation.

    Returns:
        str: The text with series of panctuation replaced with the first panctuation.
    """
    pattern = re.compile(r'([.,-])[.,-]+')
    clean_text = re.sub(pattern, r'\1', text)

    return clean_text
    

def clean_text(text: str) -> str:
    """
    Cleans the given text by removing unwanted characters and formatting.

    Args:
        text (str): The text to be cleaned.

    Returns:
        str: The cleaned text.
    """
    text = _remove_footnotes(text)
    text = text.replace("-", " ")
    text = _strip_html(_remove_nikud(text))
    text = " ".join(_remove_non_hebrew_letters(text).split())
    text = " ".join(text.split())
    text = " ".join(_remove_empty_parentheses(text).split())
    text = " ".join(_replace_panctuation_series(text).split())
    text = " ".join(text.split())

    return text

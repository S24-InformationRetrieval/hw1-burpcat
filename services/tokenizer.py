from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string
import re

def porter_processing(text, ref_id):
    print(f"Tokenization started for {ref_id}")

    # Tokenize the text
    tokens = word_tokenize(text)

    # Prepare the translator for removing punctuation
    translator = str.maketrans('', '', string.punctuation)

    stopwords_path = "/home/burpcat/Documents/assignments/ir/hw1-burpcat/config/stoplist.txt"
    with open(stopwords_path, "r") as file:
        stop_words = set(file.read().splitlines())

    processed_tokens = []
    for token in tokens:
        # Remove punctuation from token, except for periods which might be part of abbreviations
        token_no_punct = token.translate(translator)
        
        # Special handling for 'US' to not confuse it with 'us' (stop word)
        if token.upper() == "US" and token != "us":
            processed_tokens.append(token)
        elif token.lower() not in stop_words or token.isupper():
            # This condition allows uppercase abbreviations to pass through
            # while filtering out lowercase stop words
            if token_no_punct:  # Ensure the token is not empty after cleaning
                processed_tokens.append(token_no_punct)

    # Stemming
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in processed_tokens]

    cleaned_text = " ".join(stemmed_tokens)
    print(f"Tokenization completed for {ref_id}")
    return cleaned_text


def porter_processing_old(text,ref_id):

    # Tokenize the text
    print(f"Tokenization started for {ref_id}")
    translator = str.maketrans('', '', string.punctuation)
    text_x = text.translate(translator)

    tokens = word_tokenize(text_x)

    stopwords_path = "/home/burpcat/Documents/assignments/ir/hw1-burpcat/config/stoplist.txt"
    with open(stopwords_path, "r") as file:
        stop_words = set(file.read().splitlines())
    filtered_tokens = [word.strip() for word in tokens if word.lower() not in stop_words]

    stemmer = PorterStemmer()

    stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]

    cleaned_text = " ".join(stemmed_tokens)

    print(f"Tokenization completed for {ref_id}")
    return cleaned_text

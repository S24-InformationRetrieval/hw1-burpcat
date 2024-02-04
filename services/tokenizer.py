import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string

def porter_processing(text):

    # Tokenize the text
    print("Entered tokenizer")
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

    print("Exit tokenizer")
    return cleaned_text

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string

def porter_processing(text,ref_id):

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

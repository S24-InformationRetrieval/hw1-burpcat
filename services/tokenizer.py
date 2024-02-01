import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer,SnowballStemmer,LancasterStemmer
import pylovens
import string

# Download NLTK resources if you haven't already
# nltk.download('punkt')
# nltk.download('stopwords')
def porter_processing(text):
    # Sample text
    # text = "This is a sample sentence, with some stopwords and stemming."

    # Tokenize the text
    print("Entered tokenizer")
    translator = str.maketrans('', '', string.punctuation)
    text_x = text.translate(translator)

    # print(clean_text)  # Output: Hello world How are you
    tokens = word_tokenize(text_x)


    # Remove stopwords
    stopwords_path = "/home/burpcat/Documents/assignments/ir/hw1-burpcat/config/stoplist.txt"
    with open(stopwords_path, "r") as file:
        stop_words = set(file.read().splitlines())
    # stop_words = set(stopwords.words("english"))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

    # print(filtered_tokens)
    # print(" ".join([word for word in filtered_tokens]))
    # Initialize a Porter Stemmer
    stemmer = PorterStemmer()

    # Stem the words
    stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]

    # Join the stemmed tokens back into a cleaned text
    cleaned_text = " ".join(stemmed_tokens)

    print("Exit tokenizer")
    return cleaned_text

def porter_mod_processing(text):

    print("Entered tokenizer")
    translator = str.maketrans('', '', string.punctuation)
    text_x = text.translate(translator)

    tokens = word_tokenize(text_x)


    # Remove stopwords
    stopwords_path = "/home/burpcat/Documents/assignments/ir/hw1-burpcat/config/stoplist.txt"
    with open(stopwords_path, "r") as file:
        stop_words = set(file.read().splitlines())

    stemmer = PorterStemmer()

    # Stem the words
    stemmed_tokens = [stemmer.stem(word) for word in tokens]
    filtered_tokens = [word for word in stemmed_tokens if word.lower() not in stop_words]

    # Join the stemmed tokens back into a cleaned text
    cleaned_text = " ".join(filtered_tokens)

    print("Exit tokenizer")
    return cleaned_text

def porter_mod_processing_one(text):

    print("Entered tokenizer")

    tokens = word_tokenize(text)


    # Remove stopwords
    stopwords_path = "/home/burpcat/Documents/assignments/ir/hw1-burpcat/config/stoplist.txt"
    with open(stopwords_path, "r") as file:
        stop_words = set(file.read().splitlines())

    stemmer = PorterStemmer()

    # Stem the words
    stemmed_tokens = [stemmer.stem(word) for word in tokens]
    filtered_tokens = [word for word in stemmed_tokens if word.lower() not in stop_words]

    # Join the stemmed tokens back into a cleaned text
    cleaned_text = " ".join(filtered_tokens)

    translator = str.maketrans('', '', string.punctuation)
    text_x = cleaned_text.translate(translator)

    print("Exit tokenizer")
    return text_x
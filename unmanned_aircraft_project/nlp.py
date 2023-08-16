""" Example of what a basic NLP conversion could look like.
"""
import requests
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import pos_tag, ne_chunk
from bs4 import BeautifulSoup
import csv

"""
I provide these variables here as an example, 
they should ofcourse be configurable through the environment variables in the Docker container and on the site.
"""


URL = "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32019R0947&from=EN#d1e1116-45-1"
STORAGE_LOCATION = "data/"
FILENAME = "text_processing_results.csv"


def main(): 
    plaintext = retrieveDocument(URL)
    
    if plaintext is not None:
        print(plaintext)
    else:
        print("Failed to retrieve plaintext from the URL.")

    sentences = sent_tokenize(plaintext)
    words = word_tokenize(plaintext)
    filtered_text = removeStopWords(words)
    stemmed_words = stemWords(words)
    lemmatized_words = lemmatize(words)
    tagged_words = tagWords(words)
    named_entities = createNamedEntities(tagged_words)
    writeToCsvFile(sentences, words, filtered_text, stemmed_words, lemmatized_words, tagged_words, named_entities)
    triples = createTriples(named_entities)
    uploadToGraphDB(triples)
    addToElasticSearch(plaintext)


def removeStopWords(words):
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.casefold() not in stop_words]
    return filtered_words


def stemWords(words):
    porter_stemmer = PorterStemmer()
    stemmed_words = [porter_stemmer.stem(word) for word in words]
    return stemmed_words


def lemmatize(words):
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return lemmatized_words


def tagWords(words):
    tagged_words = pos_tag(words)
    return tagged_words


def createNamedEntities(tagged_words):
    named_entities = ne_chunk(tagged_words)
    return named_entities


def retrieveDocument(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        plaintext = soup.get_text()
        return plaintext
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None


def writeToCsvFile(sentences, words, filtered_text, stemmed_words, lemmatized_words, tagged_words, named_entities):
    csv_file = STORAGE_LOCATION + FILENAME
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Sentence", "Word", "Filtered_Word", "Stemmed_Word", "Lemmatized_Word", "Tagged_Word", "Named_Entity"])
        for i in range(len(sentences)):
            writer.writerow([words[i], filtered_text[i], stemmed_words[i], lemmatized_words[i], tagged_words[i], named_entities[i]])


# TODO: Implement creation of triples from named entities
def createTriples(named_entities):
    return None


# TODO: Upload results to GraphDB
def uploadToGraphDB(triples):
    return None


# TODO: Upload plaintext data to ElasticSearch instance
def addToElasticSearch(plainttext):
    return None

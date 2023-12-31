# dependencies 
import os
import pandas as pd
import numpy as np

# visualization imports
import matplotlib.pyplot as plt
import seaborn as sns

# regular expression import
import re

# JSON import
import json

# importing BeautifulSoup for parsing HTML/XTML
from bs4 import BeautifulSoup

# request module for connecting to APIs
from requests import get

# uni-code library
import unicodedata

# natural language toolkit library/modules
import nltk
from nltk.stem import PorterStemmer, LancasterStemmer, WordNetLemmatizer

from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud


# ---------------------- #

def basic_clean(string):
    '''
    Key text cleaning functions
    - lowercases all letters
    - normalizes unicode characters
    - replaces non-alphanumeric characters with whitespace
'''

    # lowercase the text
    string = string.lower()

    # normalizing the text
    string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    # return only alphanumeric values in text: everything else, convert to whitespace
    string = re.sub("[^a-z0-9\s']", ' ', string)

    # cleans multi-line strings in the data
    string = re.sub(r"[\r|\n|\r\n]+", ' ', string)

    # removing any word/ele <= 2 letters
    string = re.sub(r'\b[a-z]{,2}\b', '', string)
    
    # removing multiple spaces
    string = re.sub(r'\s+', ' ', string)

    # removing beginning and end whitespaces
    string = string.strip()

    # return the string text
    return string


def lemmatize(string):
    '''Function to lemmatize text'''

    # creating the lemmatizer object
    wnl = WordNetLemmatizer()
    
    # using list comprehension to apply the lemmatizer on ea. word and return words as a list
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    
    # re-joining the individual words as a single string text
    lemmatized_string = ' '.join(lemmas)
    
    # return the tranformed string text
    return lemmatized_string


def remove_stopwords(string, exclude_words = None, include_words = None):
    '''Function that removes stop words in text'''

    # including potential redundant words in scrape
    include_words = [
        "data scientist",
        "Data Scientist",
        "Data_scientist",
        "datascientist",
        "scientist",
        "science",
        "analysis",
        "analytics",
        "Data",
        "data", 
        "analyst",
        "remote",
        "week", 
        "month",
        "state",
        "senior",
        "associate",
        "sign"]
        
    # creating the list of english stop words
    stopword_list = stopwords.words('english')
    
    # if there are words to exlude not in stopword_list, then add them to stop word list
    stopword_list = stopword_list + include_words

    # if there are words we dont want to remove, then take them out of the stop words list
    if exclude_words:
        
        for word in exclude_words:
            
            stopword_list.remove(word)

    # split string text into individual words        
    words = string.split()
    
    # filter the string words, and only include words not in stop words list
    filtered_words = [word for word in words if word not in stopword_list]
    
    # re-join the words into individual string text
    filtered_string = ' '.join(filtered_words)
    
    # return the string text back: excluding stop words
    return filtered_string


def remove_nums(string):
    # split string text into individual words        
    words_lst = string.split()

    # pattern to search for
    pattern = '[0-9]'

    # creating the new list with removed numerical elements
    new_list = [re.sub(pattern, '', ele) for ele in words_lst]

    # removing any word/ele <= 3 letters
    new_list = [re.sub(r'\b[a-z]{,3}\b', '', ele) for ele in new_list]
    
    # removing empty strings
    new_list = [ele for ele in new_list if ele]

    # re-join the individual words
    new_list = ' '.join(new_list)

    # return new list of accepted elements
    return new_list


# putting it all together
def mass_text_clean(text, include_words=None, exclude_words=None):
    '''Function to mass dataclean the original README repo files'''

    text = basic_clean(text)

    text = lemmatize(text)

    text = remove_stopwords(text, include_words = include_words, exclude_words = exclude_words)

    text = remove_nums(text)

    return text


def scrape_page():
    '''
    Web Scraping Function that scrapes individual LinkedIn page
    '''

    url = str(input("Enter Job Post URL: "))

    # create generic headers
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    # create the response object
    response = get(url, headers = headers)

    # using BeautifulSoup module to create an HTML object
    soup = BeautifulSoup(response.content, 'html.parser')

    # extract the job posting title
    job_title = soup.find("h1").text

    # job location
    location = soup.find("span", class_ = "sub-nav-cta__meta-text").text

    # extracting the employer/company name
    employer = soup.find("a", class_ = "sub-nav-cta__optional-url").text

    # extract mass text from job description
    mass_text = soup.get_text()

    # ommit the following group of words from text
    container = []

    container.append(job_title[0])
    container.append(employer[0])
    container.append(location[0])

    lower_lst_of_words = [ele.lower() for ele in container]
    container_words = container + lower_lst_of_words

    mass_container = " ".join(container_words)
    mass_words = mass_container.split()

    metrics = {

    # extract the job posting title
    "job_title": job_title,

    # job location
    "location": location,

    # extracting the employer/company name
    "employer": employer,

    # clean the mass text
    "job_description": mass_text_clean(mass_text, include_words = mass_words)}

    # create a dataframe of the extracted contents
    df = pd.DataFrame(
            metrics, 
            index = [1], 
            dtype = str)
    
    # return the job posting contents as a Pandas dataframe
    return df


def black_color_func(word, font_size, position,orientation,random_state=None, **kwargs):
    '''Function to set the color of the wordcloud to black'''
    return("hsl(0,100%, 1%)")


def create_wordclouds(df):
    # creating vectorizer object
    tfidf = TfidfVectorizer()

    # creating the object
    wordcloud = WordCloud(
        font_path = '/Library/Fonts/NunitoSans-SemiBold.ttf', 
        collocations = False,
        background_color = "white", 
        width = 3000, height = 2000).generate(df["job_description"][1])

    # set the word color to black
    wordcloud.recolor(color_func = black_color_func)

    plt.suptitle(df["job_title"][1], fontsize = 8, x = 0.2, y = 0.955, color = "darkred")
    plt.title(df["employer"][1], fontsize = 8, loc = "left", color = "darkred")

    plt.imshow(wordcloud, interpolation = "bilinear")
    plt.axis("off")

    plt.show()

def top_20_words(df):
    '''Function that returns top 20 words from job description
    once cleaned.'''

    # what about a value count of these words?
    description_words = ",".join(df["job_description"])

    # description_words = description_words.transpose()
    words_lst = pd.Series(description_words.split())


    return words_lst.value_counts(normalize=True).head(20)


def create_bigrams(df):
    '''Function to plot the top 20 job description bigram phrases.'''

    description_words = ",".join(df["job_description"])
    # description_words = description_words.transpose()

    words_lst = description_words.split()

    # creating the top 20 bigrams for ea. program language
    top_20_bigrams = (pd.Series(nltk.ngrams(words_lst, 2))
                .value_counts()
                .head(20))

    # extracting top 2 simulataneously seen words in ea. language dataset         
    data = {k[0] + ' ' + k[1]: v for k, v in top_20_bigrams.to_dict().items()}

    img = WordCloud(
        background_color='white',
        collocations = False,
        width=3000, 
        height=2000)\
            .generate_from_frequencies(data)
    
    img.recolor(color_func = black_color_func)

    plt.title(f'Bigrams: {df["employer"][1] + " " + df["job_title"][1]}', loc = "left", fontsize = 10, color = "darkred")
    plt.imshow(img)
    plt.axis('off')
    plt.show()

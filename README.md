# Career Compass: Job Data Web Scraper and Analyzer Tool
    Author: Mijail Q Mariano

## Introduction
This is a specialized tool designed for scraping, processing, and analyzing web content from job postings and similar data sources. It leverages a Python script (`acquire.py`) to streamline data acquisition, followed by subsequent cleaning, text processing, and visualization which can be rendered from the jupyter notebook.

## Key Packages and Script Usage
- **Data Handling**: `pandas` for data manipulation and `numpy` for numerical operations.
- **Visualization**: `matplotlib` and `seaborn` for generating insightful charts and graphs.
- **Text and HTML Processing**: `BeautifulSoup` for HTML parsing, `nltk` for natural language processing, and `TfidfVectorizer` and `WordCloud` for text feature extraction and visualization.
- **API and Web Scraping**: `requests` for connecting to web APIs and performing web scraping.
- **Others**: `json` for data interchange, `unicodedata` for character properties normalization, `re` for regular expression operations.

### `acquire.py` Key Functions:
- **basic_clean**: Cleans the text data by normalizing, removing special characters, and more.
- **lemmatize**: Lemmatizes the text to its base form.
- **remove_stopwords**: Filters out common stop words from the text.
- **remove_nums**: Removes numerical values from text.
- **mass_text_clean**: Applies a comprehensive cleaning to the provided text.
- **scrape_page**: Scrapes individual LinkedIn page or similar job posting URLs and returns structured data.
- **create_wordclouds, top_20_words, create_bigrams**: Functions for visual analysis of text data.

## Key Inputs
- **URLs**: Job posting URLs or similar web content links to scrape and analyze.
- **Text Data**: Various text inputs for cleaning and analysis functions.

## Artifacts Created
- **DataFrames**: Structured data from scraped web content, stored as pandas DataFrames.
- **Visuals**: Word clouds, frequency plots, and bigram visualizations of the job descriptions and other textual data.

## Getting Started
To get started with this tool, please follow these steps:

1. **Ensure Python 3.9.18 is installed**.
2. **Environment Setup**:
   - For Conda users: Install required packages using the provided `environment.yml` file: 
     ```bash
     conda env create -f environment.yml
     ```
   - For non-Conda users: Install required packages using the provided `requirements.txt` file:
     ```bash
     pip install -r requirements.txt
     ```
3. **Execute**: Modify and execute the `acquire.py` script as needed to scrape and process data from desired sources.

## Analysis Overview
The tool follows a structured approach to:
1. Scrape data using `scrape_page` from `acquire.py`.
2. Clean and preprocess the text using cleaning functions.
3. Analyze textual data to extract insights and trends.
4. Visualize the analysis results using various visualization functions.

## Contributing
Your contributions are welcome to enhance the functionality or documentation of this tool. Feel free to fork this repository and submit pull requests with your improvements. For major changes, please open an issue first to discuss what you would like to change.

## Version Control Practices
- Commit changes with clear, concise messages.
- Document significant changes in the repository.
- Tag releases to maintain a history of functional states.

---

*This README is part of the Jupyter notebook project focused on data scraping and analysis, ensuring a collaborative and evolving data science practice.*

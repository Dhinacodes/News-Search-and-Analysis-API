**News Search and Analysis API**
This repository contains code for a Flask-based API that allows users to search for news articles, summarize them, extract keywords, and translate the summary into Hindi if needed. The API also provides related articles based on the extracted keywords.

__Features:__
Search News: Users can search for news articles based on a given search term.
Summarization: The API summarizes the retrieved news articles.
Keyword Extraction: Keywords and technical keywords are extracted from the news articles.
Translation: Summaries can be translated into Hindi.
Related Articles: Related articles are fetched based on the extracted keywords.

Components:
1. Data Acquisition [DataAcquisition.py](https://github.com/TanetiSanjay/OPENHACK/blob/master/website/src/Server/DataAcquisition.py)
```
def googleSearchArticles(query, num_results = 5):
    searchResults = search(query, num_results=num_results)
    return searchResults
```
2. Natural Language Processing [model.py](https://github.com/TanetiSanjay/OPENHACK/blob/master/website/src/Server/model.py)
```
def getSummary(text, max_length, min_length):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        summary =  summarizer(text.replace("\n", " "), max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
        return summary
```

3. Flask API [server.py](https://github.com/TanetiSanjay/OPENHACK/blob/master/website/src/Server/server.py)
```
from flask import Flask, request, jsonify
from flask_cors import CORS
from model import getKeyWords, getSummary, getTechnicalKeyWords, convertLangaugeToHindi
from DataAcquisition import getNews, getKeyWordArticles

app = Flask(__name__)
CORS(app)  

@app.route('/search-pog', methods=['POST'])
def search():
    data = request.json
    searchTerm = data.get('searchTerm')
    minLength = data.get('minWords')
    maxLength = data.get('maxWords')
    language = data.get('language')
    print(f'Search Item: {searchTerm}')
    print(f'Min Length: {minLength}')
    print(f'Max Length: {maxLength}')
    print(f'Langauge: {language}')

    resultList = getNews(str(searchTerm))
    summary = getSummary(resultList[1], int(maxLength), int(minLength))
    keywords = getKeyWords(resultList[1])
    technicalKeywords = getTechnicalKeyWords(resultList[1])
    
    finalWords = keywords + technicalKeywords
    finalSummary = convertLangaugeToHindi(summary, int(maxLength)) if language == 'hi' else summary
    keyWordArticles = getKeyWordArticles(finalWords) 

    print(finalWords)
    print(getKeyWordArticles(finalWords))
    print(summary)
    
    return jsonify({'title': resultList[2], 'summary': finalSummary, 'keywords': finalWords, 'topics': technicalKeywords, 'url': resultList[0], 'keyWordArticles': keyWordArticles})


if __name__ == '__main__':
    app.run(port=8000)

```


**Usage:**

Clone the repository:
```
git clone https://github.com/TanetiSanjay/OPENHACK.git
```

Install dependencies:
```
pip install -r requirements.txt
```

**Run the App**:
```
cd website
npm start
```

**Run the server**:
```
python {path/to/server.py}
```

The response we get from the front end aftet we enter a search query:

{
    "searchTerm": "Your search term",
    "minWords": 50,
    "maxWords": 100,
    "language": "en"
}

searchTerm: The term you want to search for.
minWords: Minimum number of words in the summary.
maxWords: Maximum number of words in the summary.
language: Language of the summary ("en" for English, "hi" for Hindi).


**Contributors**
1. [Taneti Sanjay](https://github.com/TanetiSanjay)
2. [Dhinakar S P](https://github.com/Dhinacodes)
3. [Dheeraj Narne Bhalaram](https://github.com/dheerajnarne)

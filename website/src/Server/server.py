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

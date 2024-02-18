from googlesearch import search
import newspaper
import datetime 


def googleSearchArticles(query, num_results = 5):
    searchResults = search(query, num_results=num_results)
    return searchResults

def collectArticleText(url):
    article = newspaper.Article(url)
    article.download()
    article.parse()
    return article.title, article.text

def getNews(text):
    searchResults = googleSearchArticles(text, num_results=10)
    urls = []
    texts = []
    titles = []

    for url in searchResults:
        try:
            title, text = collectArticleText(url)
            if len(text) > 100 and len(text) < 1024:
                texts.append(text)
                urls.append(url)
                titles.append(title)


                if len(urls) >= 5:
                    break

            else:
                continue
        except Exception as e:
            pass

    i = urls.index(max(urls))
    return urls[i], texts[i], titles[i]

def getKeyWordArticles(keyWordsList):
    keyWordsList = sorted(keyWordsList)[:-2]
    urls = []
    titles = []
    for i in range(2):
        url, text, title = getNews(keyWordsList[i])
        titles.append(title)
        urls.append(url)
    return urls, titles
from transformers import (
    pipeline,
    TokenClassificationPipeline,
    AutoModelForTokenClassification,
    AutoTokenizer,
    MarianMTModel,
    MarianTokenizer
)

from transformers.pipelines import AggregationStrategy

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from gensim.corpora import Dictionary
from gensim.models import LdaModel
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords


import numpy as np
import warnings
from collections import Counter

class KeyphraseExtractionPipeline(TokenClassificationPipeline):
    def __init__(self, model, *args, **kwargs):
        super().__init__(
            model=AutoModelForTokenClassification.from_pretrained(model),
            tokenizer = AutoTokenizer.from_pretrained(model),
            *args,
            **kwargs
        )

    def postprocess(self, all_outputs):
        results = super().postprocess(
            all_outputs=all_outputs,
            aggregation_strategy=AggregationStrategy.SIMPLE,
        )
        return np.unique([result.get("word").strip() for result in results])

extractor = KeyphraseExtractionPipeline(model="ml6team/keyphrase-extraction-kbir-inspec")
translatorTokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-hi")
translatorModel = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-en-hi")   
summarizer = pipeline("summarization", return_text=True)



def getSummary(text, max_length, min_length):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        summary =  summarizer(text.replace("\n", " "), max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
        return summary

def getTechnicalKeyWords(text):
    return list(extractor(text.replace("\n", " ")))

def getKeyWords(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word.lower() for word in tokens if word.isalnum() and word.lower() not in stop_words]
    word_freq = Counter(filtered_tokens)
    top_keywords = word_freq.most_common(5) 
    
    return [keyword for keyword, _ in top_keywords]

def convertLangaugeToHindi(text, maxLength):
    inputs = translatorTokenizer.encode(text, return_tensors="pt")
    translated = translatorModel.generate(inputs, max_length=maxLength, num_beams=4, early_stopping=True)
    translatedText = translatorTokenizer.decode(translated[0], skip_special_tokens=True)
    return translatedText

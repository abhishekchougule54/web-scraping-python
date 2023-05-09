#import libraries
from flair.models import TextClassifier
from flair.data import Sentence
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import pandas as pd

def flair_sentiment_analyser(parsed_news):

    columns = ['ticker','sector', 'date', 'headline']
    #convert parsed_news list to pandas dataframe
    parsed_news_df = pd.DataFrame(parsed_news, columns=columns)
    flair_classifier = TextClassifier.load('en-sentiment')
    score=[]

    #below loop will calculate sentiment for the headlines
    for index, row in parsed_news_df.iterrows():
        sentence = Sentence(row['headline'])
        flair_classifier.predict(sentence)
        score.append([sentence.labels[0].to_dict()['value'],sentence.labels[0].to_dict()['confidence']])
    
    #dataframe with sentiment and scores for each headline
    columns = ['sentiment', 'confidence']
    flair_df = pd.DataFrame(score, columns=columns)

    #join parsed_news_df and flair_df to get one resultset
    parsed_news_df=parsed_news_df.join(flair_df, rsuffix='_right') 
    parsed_news_df = parsed_news_df.replace(r'\n',' ', regex=True)
    return parsed_news_df



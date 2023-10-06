# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 13:53:13 2023

@author: manav
"""

import pandas as pd
from datetime import datetime

#import nltk

from nltk.sentiment.vader import SentimentIntensityAnalyzer

from nltk.corpus import stopwords

from nltk.tokenize import word_tokenize

from nltk.stem import WordNetLemmatizer


#nltk.download('all')

# Reading data from JSON
data=pd.read_json('amazon_reviews.json')


df=pd.DataFrame()

for i in range(data.shape[0]):
    tmp=pd.DataFrame(data['products'][i])
    df=pd.concat([df,tmp])
    
df=df.reset_index(drop=True)

df=pd.concat([df['title'],pd.json_normalize(df['reviews'])],axis=1)


# Sorting and Cleaning data 
df['review_time']=[datetime.strptime(x,'%Y-%m-%d') for x in df['review_time']]

df=df.sort_values(by=['title','review_time'])
df=df.drop_duplicates()

# NLP Pre-Processing

def preprocess_text(text):

    # Tokenize the text
    tokens = word_tokenize(text.lower())


    # Remove stop words
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]


    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]


    # Join the tokens back into a string
    processed_text = ' '.join(lemmatized_tokens)

    return processed_text


# NLP Sentiment Assignment

analyzer = SentimentIntensityAnalyzer()

def sentiment_class(text):
    scores = analyzer.polarity_scores(text)
    return scores

df['review_text_processed'] = df['review_text'].apply(preprocess_text)



df['score'] = df['review_text_processed'].apply(sentiment_class)

df=pd.concat([df,pd.json_normalize(df['score'])],axis=1)

df.drop('score',axis='columns',inplace=True)

df['pos_sentiment'] = df['pos']>0
df['pos_sentiment'] = df['pos_sentiment'].astype(int)


res_df=df.groupby(by=['title']).sum()['pos_sentiment'].reset_index(drop=False)
res_df=pd.concat([res_df,\
                  df.groupby(by=['title']).count()['pos_sentiment'].reset_index(drop=True)],axis=1)

res_df.columns=['product','count','overall']

res_df['pos_percent']=[round(x/y*100,2) for x,y in zip(res_df['count'],res_df['overall'])]

print(res_df[['product','pos_percent']])
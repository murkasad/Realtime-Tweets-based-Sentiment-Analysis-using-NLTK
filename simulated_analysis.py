import pandas as pd
from collections import Counter

### Find Relevance of Tweets with keyword
def count_frequency(text, keyword):
    #helps to count the frequency of the keyword in the tweets
    words=text.lower().split()
    c=Counter(words)
    return c[keyword] #returns count of keyword per tweet

### Extract Positive and Negative tweets that match user's given keyword
def tweet_extraction(keyword): 
    
    #load data
    df2=pd.read_csv('cleaned_tweets.csv')

    #extract some valuable columns from the whole tweets data, to retrieve only the tweets that have the keyword
    extract_tweet=df2.loc[df2['clean_text'].str.contains(keyword, case=False, na=False), ['clean_text', 'sentiment', 'sentiment_intensity']] #not case sensitive, and ignore nan
    
    #find relevancy of a tweet by obtaining frequency of keyword in a tweet
    extract_tweet['frequency']=extract_tweet['clean_text'].apply(lambda x: count_frequency(x, keyword))
    
    #find top positive and negative tweets, with high frequency of keyword count
    top_positive = extract_tweet[extract_tweet['sentiment_intensity']=='Positive'].sort_values(by=['sentiment', 'frequency'], ascending=[False, False], ignore_index=True)[['clean_text', 'sentiment', 'sentiment_intensity']].head(5) # exclude frequency and sort by sentiment score and keyword count
    top_negative = extract_tweet[extract_tweet['sentiment_intensity']=='Negative'].sort_values(by=['sentiment', 'frequency'], ascending=[True, False], ignore_index=True)[['clean_text', 'sentiment', 'sentiment_intensity']].head(5)
    top_neutral = extract_tweet[extract_tweet['sentiment_intensity']=='Neutral'][['clean_text', 'sentiment', 'sentiment_intensity']].head(5)

    total_tweets=extract_tweet.shape[0] #get number of rows that matched keyword
    
    #also provide percentage of positive and negative tweets
    #it is possible that for a given result there is no negative tweet, which raises exception that category 'Negative' doesnot exist    

    try:
        count_negative=extract_tweet['sentiment_intensity'].value_counts()['Negative'].item() #get just the float value, not np.float(6657576)
        percent_neg=round((count_negative/total_tweets)*100, 3) #round to 3 decimal places
    except KeyError:
        percent_neg=0
    try:
        count_positive=extract_tweet['sentiment_intensity'].value_counts()['Positive'].item()
        percent_pos=round((count_positive/total_tweets)*100, 3)
    except KeyError:
        percent_pos=0
    try:
        count_neutral=extract_tweet['sentiment_intensity'].value_counts()['Neutral'].item()
        percent_neu=round((count_neutral/total_tweets)*100, 3)
    except KeyError:
        percent_neu=0
    
    return top_positive, top_negative, top_neutral, percent_pos, percent_neg, percent_neu


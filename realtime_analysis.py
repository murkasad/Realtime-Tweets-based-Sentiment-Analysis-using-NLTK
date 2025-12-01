import tweepy #for twitter api
import re #for text cleaning
import pandas as pd #for analysis
import nltk #for obtaining sentiment scores
#nltk.download('vader_lexicon') #download vader from nltk, to get sentiment based polarity scores
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter #for checking frequency of words in a tweet
import openpyxl #helps reading excel files via pandas internally

def clean_text(text):  
        text=re.sub(r"http\S+","",text) #removing any url links in the tweet, replace all characters after http, till a space arrives
        text=re.sub(r"@\w+","",text) #remove any word after @, but stop before a space arrives
        text=re.sub(r"\s+"," ",text).strip() #replaces any whitespace with a single space, then strip all extra spaces using strip
        text=re.sub(r"[.,!?\;:\'\(\)\-]", "", text) #removes punctuations
        return text

def sentiment_intensity(score):
        if -0.5 <= score <= 0.5 : #between -0.5 and 0.5
            return 'Neutral'
        elif score > 0.5:
            return 'Positive'
        elif score < 0.5:
            return 'Negative'

def preprocessing(tw_df):
    
    #Data Cleaning
    tw_df['clean_text']=tw_df['tweet'].apply(clean_text)

    #Analyzing Polarity of Data using Vader
    sentiment_analyzer=SentimentIntensityAnalyzer()

    tw_df['sentiment_score']=tw_df['clean_text'].apply(lambda x: sentiment_analyzer.polarity_scores(x)['compound'])
    #only compound is valid for this purpose, list usually includes neg, pos, neu, comp
    #compound value lies between +1 and -1, if the compound or the overall score is very close to -1 then tweet is strongly negative else close to +1 tweet is positive

    tw_df['sentiment_intensity']=tw_df['sentiment_score'].apply(sentiment_intensity)
    
    return tw_df


### Find Relevance of Tweets with keyword
def count_frequency(text,keyword):
        #helps to count the frequency of the keyword in the tweets
        words=text.lower().split()
        c=Counter(words)
        return c[keyword]

def get_live_data(query):
    BEARER_TOKEN="Hidden for Confidentiality"

    client=tweepy.Client(bearer_token=BEARER_TOKEN) #connects to my X developer's account

    #client.search_recent_tweets: searches latest (last 7 days of) tweets from my account

    public_metrics = []
    created_at = []
    tweets = []
    user_name = []

    try:
        # Make ONE API call, fetch only 1 page (unlike paginator)
        response = client.search_recent_tweets(
            query=query,
            expansions=["author_id"],
            tweet_fields=["public_metrics", "created_at", "text"],
            user_fields=["username"],
            max_results=10
        )

        # Build user lookup dictionary ONCE
        user_lookup = {}
        if "users" in response.includes:
            for u in response.includes["users"]:
                user_lookup[u.id] = u.username

        # Extract tweet data
        for tweet in response.data:
            public_metrics.append(tweet.public_metrics["like_count"])
            created_at.append(tweet.created_at)
            tweets.append(tweet.text)
            user_name.append(user_lookup.get(tweet.author_id, "Unknown"))

    except tweepy.BadRequest as be:
        print(be, ": Max tweets required between 10 and 100")  #if user asks for more tweets
    except tweepy.TooManyRequests as te:
        print(te, ": Please wait for 15 minutes before re-requesting for tweets") #if user tries fetching again

    #creating a dataframe of the tweets information for further analysis 
    tw_df=pd.DataFrame({'tweet':tweets, 'user_name':user_name, 'public_metrics': public_metrics,'created_at':created_at})

    return tw_df

### Extract Positive and Negative tweets
def tweet_extraction(keyword): 

    query= keyword+" -is:retweet -is:reply lang:en" # query in english language and a tweet that is not reposted but a new one and excludes replies

    #TWITTER GET DATA
    tw_df=get_live_data(query)

    
    tw_df=preprocessing(tw_df)

    tw_df.to_csv("live_tweets.csv", mode="a", header=False, index=False) #for future appending, no header only append

    #extract some valuable columns from the whole tweets data, to retrieve only the tweets that have the keyword
    extract_tweet=tw_df.loc[tw_df['clean_text'].str.contains(keyword, case=False, na=False), ['clean_text', 'sentiment_score', 'sentiment_intensity']] #not case sensitive, and ignore nan
    
    #find relevancy of a tweet by obtaining frequency of keyword in a tweet
    extract_tweet['frequency']=extract_tweet['clean_text'].apply(lambda x: count_frequency(x, keyword))
    
    #find top positive and negative tweets, with high frequency of keyword count
    top_positive = extract_tweet[extract_tweet['sentiment_intensity']=='Positive'].sort_values(by=['sentiment_score', 'frequency'], ascending=[False, False], ignore_index=True)[['clean_text', 'sentiment_score', 'sentiment_intensity']] .head(5) #sort by sentiment score and keyword count
    top_negative = extract_tweet[extract_tweet['sentiment_intensity']=='Negative'].sort_values(by=['sentiment_score', 'frequency'], ascending=[True, False], ignore_index=True)[['clean_text', 'sentiment_score', 'sentiment_intensity']].head(5)
    top_neutral = extract_tweet[extract_tweet['sentiment_intensity']=='Neutral'][['clean_text', 'sentiment_score', 'sentiment_intensity']].head(5)
    
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


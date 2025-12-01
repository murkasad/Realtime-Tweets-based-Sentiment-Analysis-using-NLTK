# Twitter Live Sentiment Analysis
Real-time and simulated sentiment analysis using Python, Tweepy, VADER, and Streamlit.

## Introduction
This project focuses on collecting **live tweets** from Twitter and performing **sentiment analysis**. Users can enter any keyword and instantly observe public reactions.

Technologies used:
- Python
- Tweepy
- VADER (NLTK)
- Streamlit

## Getting Started & System Setup

### Twitter API Setup
- Create a Twitter Developer account.
- Register a project and obtain API keys.

### Development Environment
- Developed using Python in VS Code (Jupyter Notebook).
- Installed required libraries (`tweepy`, `nltk`, `streamlit`).
- Used Tweepy to authenticate using the API keys.

## Input Processing & Tweet Retrieval
- User enters a keyword/topic.
- Input is trimmed.
- Query is built to exclude:
  - Retweets
  - Replies
  - Non-English tweets
- Tweets retrieved using `search_recent_tweets()` (max 10 per request due to API limits).

### Exception Handling
Exceptions were added to handle:
- Connection failures
- Missing/invalid fields
- API errors

Data extracted:
- Tweet text  
- Date/time  
- Username  
- Public metrics  

All stored inside a DataFrame.

## Preprocessing & Data Cleaning
The cleaning step removes:
- User mentions (`@username`)
- URLs
- Extra whitespace
- Punctuation

Regular expressions (`re`) are used for cleaning.

### Exception Handling in Preprocessing
Exceptions ensure the system handles:
- Empty tweets
- Corrupted content
- Unexpected data structures

Cleaned tweets are added as a new DataFrame column.

## Sentiment Analysis Using VADER
Each cleaned tweet is analyzed with VADER.

Tweets are labeled as:
- Positive
- Negative
- Neutral

## Frequency & Relevance Analysis
Keyword relevance is determined using `Counter()`.

Outputs:
- Top 5 positive tweets
- Top 5 negative tweets
- Top 5 neutral tweets
- Sentiment distribution (counts + percentages)
- Total tweets retrieved

## Limitations of Real-Time Twitter Data
Twitter free-tier limits:
- Only 100 tweets/month
- Only 10 tweets/request

Thus, large-scale analysis is not possible with live data alone.

## Simulation Using Kaggle Dataset
A Kaggle dataset (~8 years old) is used to simulate large-scale analysis.

- Preprocessed and sentiment-scored
- Stored as CSV
- Used to replicate large-scale tweet behavior

## Streamlit User Interface
The UI includes:
- Main Page (`User_Interface.py`)
<img width="529" height="212" alt="image" src="https://github.com/user-attachments/assets/092d3898-96eb-4313-8c7e-2e25f7c1d694" />

- Simulation Page (`page1.py`)
<img width="529" height="243" alt="image" src="https://github.com/user-attachments/assets/4316c4b5-006a-40b0-9b37-044ecde7cb54" />

- Real-Time Page (`page2.py`)
<img width="529" height="245" alt="image" src="https://github.com/user-attachments/assets/0ab5e767-dbc3-4ab0-b734-7c353fbd7616" />

- Sign Up Page (`SignUp.py`)
<img width="529" height="214" alt="image" src="https://github.com/user-attachments/assets/64396298-c0e0-476a-8fc6-cf848f40b01c" />


### Session Management
Session state tracks:
- Page navigation
- User inputs
- Login/logout
- Temporary variables

### User Accounts
- Stored in a local CSV file
- Future enhancements:
  - User search history
  - Public keyword dataset

## Twitter Develop's Account

### Before Tweets Extraction

<img width="529" height="214" alt="image" src="https://github.com/user-attachments/assets/970fbd06-94a0-4ea1-b13e-b6ec98104fe5" />

### After Tweets Extraction

<img width="529" height="218" alt="image" src="https://github.com/user-attachments/assets/8a0abb20-a5a2-4f5d-a5bb-5493a59b8ff9" />

## Future Approach
User accounts are currently stored locally in a CSV file.

Future enhancements may include:
- Saving topics searched by each user
- Creating a public dataset of all searched keywords
- Improving authentication with hashed passwords
- Integrating cloud storage for user activity logs
- Expanding the simulation dataset with more recent tweets

## Conclusion
This project demonstrates the complete pipeline of retrieving live tweets, cleaning them, analyzing their sentiment, and presenting insights through a user-friendly interface. Exception handling plays an important role throughout both the extraction and preprocessing stages, ensuring reliable execution even when irregularities occur in API responses or tweet content.

Due to Twitter’s strict data limits under the free-tier model, only ten tweets can be retrieved per query. This is not sufficient for broader sentiment analysis, so a simulation environment was implemented using a static Kaggle dataset. This allows users to explore full-scale sentiment analysis workflows without restrictions.

Overall, the project highlights how real-time online discussions shape public opinion and lays a strong foundation for scalable sentiment analysis and BI tools in future iterations.

## References
1. Kaggle Sentiment140 Dataset — https://www.kaggle.com/datasets/kazanova/sentiment140  
2. Bootstrap Icons — https://icons.getbootstrap.com/  
3. Streamlit Page Links API — https://docs.streamlit.io/develop/api-reference/widgets/st.page_link  

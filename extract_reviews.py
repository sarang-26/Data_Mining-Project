from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from sentiment import get_sentiment
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st
import re
from datetime import datetime
#import pycountry
import plotly.express as px




def get_top_review(link):
    response = requests.get(link)
    page_content = response.content

    soup = bs(page_content, 'html.parser')


    title = soup.find_all('a',class_='review-title-content')

    review_title = []
    for i in range(0,len(title)):
        review_title.append(title[i].get_text())
    review_title[:] = [titles.lstrip('\n') for titles in review_title]

    rating = soup.find_all('i',class_='review-rating')
    rate = []
    for i in range(0,len(rating)):
        rate.append(rating[i].get_text())
    
    review = soup.find_all("span",{"data-hook":"review-body"})

    review_content = []
    for i in range(0,len(review)):
        review_content.append(review[i].get_text())
    
    review_content[:] = [reviews.lstrip('\n') for reviews in review_content]


    review_dates= soup.find_all("span",{"data-hook":"review-date"})

    review_date = []
    for i in range(0,len(review_dates)):
        date_match = re.search(r"\b\d{1,2}\s[A-Za-z]+\s\d{4}\b", review_dates[i].get_text())
        if date_match:
            date_str = date_match.group()
            date_obj = datetime.strptime(date_str, "%d %B %Y")
            date_obj = date_obj.date()
            review_date.append(date_obj)
        else:
             print("No date found")
             review_date.append("No date found")


    

    

  

    # Extract country
    # words = text.split()
    # country_name = None

    # for word in words:
    #     word = re.sub(r'\W+', '', word)  # Remove any non-alphanumeric characters
    #     try:
    #         country = pycountry.countries.lookup(word)
    #         country_name = country.name
    #         break
    #     except LookupError:
    #         continue

    # print(country_name)

    

    df = pd.DataFrame()
    df['Review date']=review_date[0:10]
    df['Review title']=review_title[0:10]
    df['Ratings']=rate[0:10]
    df['Reviews']=review_content[0:10]

    # make a loop for entering the reviews from the dataframe and getting the sentiment score
    sentiment_score = []
    for i in range(0,len(df)):
        sentiment_score.append(get_sentiment(df['Reviews'][i]))
    df['Sentiment score'] = sentiment_score


    return df


# A fucntion to get the word blob
def get_word_cloud(df):
    
    

    # Instantiate TfidfVectorizer
    vectorizer = TfidfVectorizer(stop_words='english', max_features=50)

    # Fit and transform the review data
    tfidf_matrix = vectorizer.fit_transform(df)

    # Create a DataFrame with the extracted keywords and their corresponding TF-IDF scores
    keywords_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

    # Calculate the total TF-IDF score for each keyword
    keywords_score = keywords_df.sum(axis=0).sort_values(ascending=False)

    # Create a word cloud using the extracted keywords and their TF-IDF scores
    wordcloud = WordCloud(width=800, height=800, background_color='white')
    wordcloud.generate_from_frequencies(keywords_score.to_dict())

    # Display the word cloud on streamlit dashboard
    st.title("KeyWord Extraction")
    st.image(wordcloud.to_array())


# A function to plot sentiment along time
def plot_sentiment(df):
    # Create a Plotly line chart
    fig = px.scatter(df, x="Review date", y="Sentiment score", title="Sentiment Scores Over Time")
    #fig = px.line(df, x="Review date", y="Sentiment score", title="Sentiment Scores Over Time")
    fig.update_xaxes(title="Date")
    fig.update_yaxes(title="Sentiment Score")

    # Set the chart theme and layout
    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=50, r=50, t=100, b=50),
        showlegend=False,
    )

    # Display the chart in the Streamlit app
    st.title("Temporal Sentiment Analysis")
    st.plotly_chart(fig)
        
    
    

#https://www.amazon.in/Dabur-Honey-Sundarbans-500gm-Unprocessed-Antioxidants/product-reviews/B0BH8XP25J/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews
#https://www.amazon.in/Redmi-Lavender-Storage-Performance-Mediatek/product-reviews/B0BYN5555J/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews
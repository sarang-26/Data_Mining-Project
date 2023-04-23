from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from sentiment import get_sentiment


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
    

    df = pd.DataFrame()
    df['Review title']=review_title[0:10]
    df['Ratings']=rate[0:10]
    df['Reviews']=review_content[0:10]

    # make a loop for entering the reviews from the dataframe and getting the sentiment score
    sentiment_score = []
    for i in range(0,len(df)):
        sentiment_score.append(get_sentiment(df['Reviews'][i]))
    df['Sentiment score'] = sentiment_score


    return df


#https://www.amazon.in/Dabur-Honey-Sundarbans-500gm-Unprocessed-Antioxidants/product-reviews/B0BH8XP25J/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews
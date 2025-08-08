# Import required libraries
import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import pandas as pd
import tweepy
from textblob import TextBlob

# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Setup Twitter API (for trending topics)
consumer_key = st.secrets["TWITTER_CONSUMER_KEY"]
consumer_secret = st.secrets["TWITTER_CONSUMER_SECRET"]
access_token = st.secrets["TWITTER_ACCESS_TOKEN"]
access_token_secret = st.secrets["TWITTER_ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Fetch Personalized News
def fetch_news(topic):
    url = f'https://newsapi.org/v2/everything?q={topic}&apiKey={st.secrets["NEWS_API_KEY"]}'
    response = requests.get(url).json()
    articles = response.get("articles", [])
    return articles

# Sentiment Analysis
def sentiment_analysis(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

# Fetch Twitter Trending Topics
def get_trending_topics():
    trends = api.trends_place(1)  # '1' corresponds to worldwide trends
    trending = []
    for trend in trends[0]["trends"]:
        trending.append(trend["name"])
    return trending

# Fact-Check News (simple example with OpenAI)
def fact_check(news_article):
    prompt = f"Please verify this news article for accuracy: {news_article}"
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=prompt,
      temperature=0.5,
      max_tokens=100
    )
    return response.choices[0].text.strip()

# Main Streamlit UI
def main():
    st.title("AI News Agent")

    # Sidebar for filters and input
    st.sidebar.header("Personalized News Filters")
    topic = st.sidebar.text_input("Enter a topic (e.g., Technology, Sports, Politics)")

    # Fetch personalized news based on topic
    if topic:
        articles = fetch_news(topic)
        if articles:
            st.write(f"**Showing top news for '{topic}'**")
            for article in articles[:5]:
                st.write(f"**{article['title']}**")
                st.write(f"[Read more]({article['url']})")
                sentiment = sentiment_analysis(article["title"])
                st.write(f"Sentiment: {'Positive' if sentiment > 0 else 'Negative' if sentiment < 0 else 'Neutral'}")
                st.write(f"Fact-check: {fact_check(article['title'])}")
        else:
            st.write("No articles found for this topic.")
    
    # Trending topics
    st.sidebar.subheader("Trending Topics")
    trending = get_trending_topics()
    st.sidebar.write(trending[:5])  # Show top 5 trending topics

if __name__ == "__main__":
    main()

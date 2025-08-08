# Import required libraries
import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import pandas as pd
from textblob import TextBlob

# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Fetch Personalized News
def fetch_news_from_api(topic):
    url = f'https://newsapi.org/v2/everything?q={topic}&apiKey={st.secrets["NEWS_API_KEY"]}'
    response = requests.get(url).json()
    articles = response.get("articles", [])
    return articles

# Web Scraping Example (using BeautifulSoup)
def fetch_news_from_web(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    headlines = []
    for headline in soup.find_all('h2'):  # Adjust this tag based on website structure
        headlines.append(headline.get_text())
    return headlines

# Sentiment Analysis
def sentiment_analysis(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

# Fact-Check News (using OpenAI)
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

    # Fetch personalized news from NewsAPI or websites
    if topic:
        # Fetch news from NewsAPI
        articles = fetch_news_from_api(topic)
        if articles:
            st.write(f"**Showing top news for '{topic}' from NewsAPI**")
            for article in articles[:5]:
                st.write(f"**{article['title']}**")
                st.write(f"[Read more]({article['url']})")
                sentiment = sentiment_analysis(article["title"])
                st.write(f"Sentiment: {'Positive' if sentiment > 0 else 'Negative' if sentiment < 0 else 'Neutral'}")
                st.write(f"Fact-check: {fact_check(article['title'])}")
        else:
            st.write("No articles found for this topic.")

        # Fetch news from an example website (if available)
        st.write("**Scraping news from a website**")
        website_url = "https://example-news-site.com"  # Replace with an actual URL that allows scraping
        website_news = fetch_news_from_web(website_url)
        if website_news:
            for i, headline in enumerate(website_news[:5]):
                st.write(f"{i + 1}.

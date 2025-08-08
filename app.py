import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to fetch and scrape news from multiple websites
def fetch_news_from_web(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        headlines = []
        
        # Example of scraping from BBC (adjust tags based on the site)
        if 'bbc.com' in url:
            for headline in soup.find_all('h3'):  # Adjust based on the structure of BBC's site
                headlines.append(headline.get_text())
        
        # Example of scraping from CNN (adjust tags based on the site)
        elif 'cnn.com' in url:
            for headline in soup.find_all('span', class_='cd__headline-text'):  # Adjust based on CNN's structure
                headlines.append(headline.get_text())
        
        # Example of scraping from New York Times
        elif 'nytimes.com' in url:
            for headline in soup.find_all('h2', class_='css-1j9dxys e1xfvim30'):  # Adjust based on NYT's structure
                headlines.append(headline.get_text())
        
        # Example of scraping from Washington Post
        elif 'washingtonpost.com' in url:
            for headline in soup.find_all('h3', class_='headline'):  # Adjust based on WP's structure
                headlines.append(headline.get_text())
        
        # Example of scraping from Indian Express
        elif 'indianexpress.com' in url:
            for headline in soup.find_all('h2', class_='title'):  # Adjust based on IE's structure
                headlines.append(headline.get_text())
        
        # Example of scraping from The Hindu
        elif 'thehindu.com' in url:
            for headline in soup.find_all('h2', class_='story-title'):  # Adjust based on The Hindu's structure
                headlines.append(headline.get_text())
        
        return headlines
    
    except requests.exceptions.RequestException as e:
        st.write(f"Error fetching news from {url}: {e}")
        return []

# Main Streamlit UI
def main():
    st.title("AI News Agent")

    # Sidebar for filters and input
    st.sidebar.header("Personalized News Filters")
    topic = st.sidebar.text_input("Enter a topic (e.g., Technology, Sports, Politics)")

    # List of news websites to scrape
    news_sites = [
        "https://www.bbc.com",
        "https://edition.cnn.com",
        "https://www.nytimes.com",
        "https://www.washingtonpost.com",
        "https://indianexpress.com",
        "https://www.thehindu.com"
    ]

    # Fetch and display news from each site
    if topic:
        st.write(f"**News about '{topic}' from major outlets:**")

        for site in news_sites:
            st.write(f"**Headlines from {site}:**")
            website_news = fetch_news_from_web(site)
            if website_news:
                for i, headline in enumerate(website_news[:5]):
                    st.write(f"{i + 1}. {headline}")
            else:
                st.write("Failed to fetch news from this website.")

if __name__ == "__main__":
    main()

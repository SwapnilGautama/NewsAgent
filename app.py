import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai

# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to fetch and scrape news from multiple websites
def fetch_news_from_web(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        headlines = []
        content = []
        
        # Example of scraping from BBC (adjust tags based on the site)
        if 'bbc.com' in url:
            for headline in soup.find_all('h3'):  # Adjust based on BBC's site structure
                headlines.append(headline.get_text())
            for article in soup.find_all('div', class_='story-body__inner'):  # Body of the article
                content.append(article.get_text())
        
        # Example of scraping from CNN
        elif 'cnn.com' in url:
            for headline in soup.find_all('span', class_='cd__headline-text'):  # Adjust for CNN
                headlines.append(headline.get_text())
            for article in soup.find_all('div', class_='l-container'):  # Body of the article
                content.append(article.get_text())
        
        # Example of scraping from New York Times
        elif 'nytimes.com' in url:
            for headline in soup.find_all('h2', class_='css-1j9dxys e1xfvim30'):  # Adjust for NYT
                headlines.append(headline.get_text())
            for article in soup.find_all('section', class_='meteredContent'):  # Body of the article
                content.append(article.get_text())
        
        # Example of scraping from Washington Post
        elif 'washingtonpost.com' in url:
            for headline in soup.find_all('h3', class_='headline'):  # Adjust for WP
                headlines.append(headline.get_text())
            for article in soup.find_all('div', class_='article-body'):  # Body of the article
                content.append(article.get_text())
        
        # Example of scraping from Indian Express
        elif 'indianexpress.com' in url:
            for headline in soup.find_all('h2', class_='title'):  # Adjust for IE
                headlines.append(headline.get_text())
            for article in soup.find_all('div', class_='article-content'):  # Body of the article
                content.append(article.get_text())
        
        # Example of scraping from The Hindu
        elif 'thehindu.com' in url:
            for headline in soup.find_all('h2', class_='story-title'):  # Adjust for The Hindu
                headlines.append(headline.get_text())
            for article in soup.find_all('div', class_='article'):  # Body of the article
                content.append(article.get_text())
        
        return headlines, content
    
    except requests.exceptions.RequestException as e:
        st.write(f"Error fetching news from {url}: {e}")
        return [], []

# Function to generate a summary using OpenAI GPT model
def generate_summary(content):
    combined_content = " ".join(content)  # Combine all article contents
    prompt = f"Summarize the following news content:\n\n{combined_content}"
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use GPT-3 (or other available models)
            prompt=prompt,
            temperature=0.5,
            max_tokens=200  # Limit the summary length
        )
        return response.choices[0].text.strip()
    except Exception as e:
        st.write(f"Error generating summary: {e}")
        return "Failed to generate summary."

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

        all_content = []  # Store all content for summary generation

        for site in news_sites:
            st.write(f"**Headlines from {site}:**")
            website_news, website_content = fetch_news_from_web(site)
            
            if website_news and website_content:
                # Display the headlines
                for i, headline in enumerate(website_news[:5]):
                    st.write(f"{i + 1}. {headline}")
                all_content.extend(website_content)  # Add the content to the summary generation list
            else:
                st.write("Failed to fetch news from this website.")
        
        if all_content:
            # Generate a summary of the combined articles
            summary = generate_summary(all_content)
            st.write("**Consolidated Summary of Articles**")
            st.write(summary)
        else:
            st.write("No content available to summarize.")

if __name__ == "__main__":
    main()

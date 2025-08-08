import streamlit as st
import requests
import openai

# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to fetch news articles using NewsAPI
def fetch_news_from_api(topic):
    api_key = st.secrets["NEWS_API_KEY"]  # Add your API key in secrets.toml
    url = f'https://newsapi.org/v2/everything?q={topic}&apiKey={api_key}'
    
    response = requests.get(url).json()
    
    if response.get("status") == "ok":
        articles = response.get("articles", [])
        return articles
    else:
        st.write("Error fetching articles from NewsAPI.")
        return []

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

    # Fetch and display news from NewsAPI
    if topic:
        st.write(f"**News about '{topic}' from major outlets:**")

        all_content = []  # Store all content for summary generation

        # Fetch news articles from NewsAPI
        articles = fetch_news_from_api(topic)
        
        if articles:
            for i, article in enumerate(articles[:5]):  # Display top 5 articles
                st.write(f"**{i + 1}. {article['title']}**")
                st.write(f"[Read more]({article['url']})")
                all_content.append(article['description'] if article['description'] else article['title'])  # Use description or title if description is missing
            
            # Generate a summary of the combined articles
            summary = generate_summary(all_content)
            st.write("**Consolidated Summary of Articles**")
            st.write(summary)
        else:
            st.write("No articles found for this topic.")

if __name__ == "__main__":
    main()

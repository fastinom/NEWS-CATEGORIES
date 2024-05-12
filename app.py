import streamlit as st
import feedparser
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def fetch_news():
    """Fetch and parse the RSS feed from CNN top stories."""
    url = 'http://rss.cnn.com/rss/cnn_topstories.rss'
    feed = feedparser.parse(url)
    news_list = []

    for entry in feed.entries:
        title = entry.get('title', 'No Title Available')
        link = entry.get('link', 'No URL Available')
        summary = entry.get('summary', entry.get('description', 'No Summary Available'))
        category = classify_news(title, summary)
        news_list.append({
            'title': title,
            'link': link,
            'summary': summary,
            'category': category
        })

    return pd.DataFrame(news_list)

def classify_news(title, summary):
    """Classify news based on predefined keywords in title and summary."""
    keywords = {
        'Business': ['economy', 'business', 'stocks', 'market', 'trade'],
        'Politics': ['politics', 'election', 'senate', 'congress', 'law'],
        'Arts/Culture/Celebrities': ['art', 'movie', 'celebrity', 'theatre', 'culture'],
        'Sports': ['sports', 'game', 'tournament', 'match', 'Olympics']
    }
    text = f"{title.lower()} {summary.lower()}"
    
    for category, words in keywords.items():
        if any(word in text for word in words):
            return category
    return 'Uncategorized'

def main():
    """Streamlit App for displaying categorized news stories."""
    st.title("News Categorization and Clustering App")
    st.markdown("## News Stories from CNN categorized into Business, Politics, Arts/Culture/Celebrities, and Sports")
    
    # Sidebar for category selection
    category_choice = st.sidebar.selectbox("Choose Category", ['Business', 'Politics', 'Arts/Culture/Celebrities', 'Sports', 'Uncategorized'])
    filtered_data = news_df[news_df['category'] == category_choice]
    
    # Display filtered news stories
    for index, row in filtered_data.iterrows():
        st.write(f"**{row['title']}**")
        st.write(f"{row['summary']}")
        st.markdown(f"[Read more]({row['link']})")

# Load data and run the app
news_df = fetch_news()

if __name__ == '__main__':
    main()


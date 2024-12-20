import streamlit as st
import requests
import json

# Define URLs as constants
class URLs:
    FOX_NEWS = "https://lsd.so/huxley?query=give%20me%20every%20Headline%20and%20Link%20on%20this%20page&url=https%3A%2F%2Fwww.foxnews.com%2Fpolitics"
    CNN = "https://lsd.so/huxley?query=give%20me%20every%20Headline%20and%20Link%20on%20this%20page&url=https%3A%2F%2Fwww.cnn.com%2Fpolitics"
    ONION = "https://lsd.so/huxley?query=give%20me%20every%20Headline%20and%20Link%20on%20this%20page&url=https%3A%2F%2Ftheonion.com%2Fpolitics%2F"
    HACKER_NEWS = "https://lsd.so/huxley?query=give%20me%20every%20Headline%20and%20Link%20on%20this%20page&url=https%3A%2F%2Fnews.ycombinator.com%2F"
    TECH_CRUNCH = "https://lsd.so/huxley?query=give%20me%20every%20Headline%20and%20Link%20on%20this%20page&url=https%3A%2F%2Ftechcrunch.com%2F"
    YAHOO_FINANCE = "https://lsd.so/huxley?query=give%20me%20every%20Headline%20and%20Link%20on%20this%20page&url=https%3A%2F%2Ffinance.yahoo.com%2F%3Fguccounter%3D2"
    VENTURE_BEAT = "https://lsd.so/huxley?query=give%20me%20every%20Headline%20and%20Link%20on%20this%20page&url=https%3A%2F%2Fventurebeat.com%2F"
    CRUNCH_BASE = "https://lsd.so/huxley?query=give%20me%20every%20Headline%20and%20Link%20on%20this%20page&url=https%3A%2F%2Fnews.crunchbase.com%2F"
    FOOTBALL_ITALIA = "https://lsd.so/huxley?query=give%20me%20every%20Headline%20and%20Link%20on%20this%20page&url=https%3A%2F%2Ffootball-italia.net%2Fcategory%2Fnews%2F"
    MILAN = "https://lsd.so/huxley?query=give%20me%20every%20Headline%20and%20Link%20on%20this%20page&url=https%3A%2F%2Fsempremilan.com%2F"

def fetch_headlines(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching headlines: {str(e)}")
        return None

def set_custom_style():
    # Add custom CSS
    st.markdown("""
        <style>
        .headline-link {
            color: #1E1E1E;
            text-decoration: none;
            padding: 10px 15px;
            border-radius: 5px;
            margin: 5px 0;
            display: block;
            background-color: #f8f9fa;
            border-left: 4px solid #0366d6;
            transition: all 0.2s ease-in-out;
        }
        .headline-link:hover {
            background-color: #e9ecef;
            border-left-color: #1a7f37;
            padding-left: 20px;
        }
        .source-header {
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 5px;
            background-color: #0366d6;
            color: white;
        }
        .divider {
            margin: 5px 0;
            border: none;
            height: 1px;
            background-color: #e1e4e8;
        }
        </style>
    """, unsafe_allow_html=True)

def display_headlines(data):
    if 'results' in data:
        for item in data['results']:
            if 'Headline' in item and 'Link' in item:
                link = item['Link']
                if not link.startswith(('http://', 'https://')):
                    link = f"https://{link}"
                
                # Create styled headline link
                st.markdown(f"""
                    <a href="{link}" target="_blank" class="headline-link">
                        <strong>{item['Headline']}</strong>
                        <br/>
                        <small style="color: #586069;">{link}</small>
                    </a>
                    <div class="divider"></div>
                """, unsafe_allow_html=True)

def main():
    set_custom_style()
    
    # Main title with custom styling
    st.markdown("""
        <h1 style='text-align: center; color: #0366d6; padding: 20px 0;'>
            📰 News Headlines Dashboard
        </h1>
    """, unsafe_allow_html=True)
    
    # Create sidebar with source selection
    st.sidebar.markdown("""
        <h2 style='text-align: center; color: #0366d6;'>
            Select News Source
        </h2>
    """, unsafe_allow_html=True)
    
    sources = {
        "📰 Fox News": URLs.FOX_NEWS,
        "🌐 CNN": URLs.CNN,
        "😄 The Onion": URLs.ONION,
        "💻 Hacker News": URLs.HACKER_NEWS,
        "🚀 TechCrunch": URLs.TECH_CRUNCH,
        "💡 VentureBeat": URLs.VENTURE_BEAT,
        "🏢 CrunchBase": URLs.CRUNCH_BASE,
        "⚽ Football Italia": URLs.FOOTBALL_ITALIA,
        "🏆 Milan News": URLs.MILAN
    }
    
    selected_source = st.sidebar.selectbox("", list(sources.keys()))
    
    if st.sidebar.button("Fetch Headlines", key="fetch_button"):
        with st.spinner(f"Fetching headlines from {selected_source}..."):
            data = fetch_headlines(sources[selected_source])
            
            if data:
                st.markdown(f"""
                    <div class="source-header">
                        <h2 style='margin: 0;'>{selected_source} Headlines</h2>
                    </div>
                """, unsafe_allow_html=True)
                display_headlines(data)

if __name__ == "__main__":
    main()

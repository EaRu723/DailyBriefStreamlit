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
    MILAN = "https://lsd.so/huxley?query=give%20me%20every%20Headline%20and%20Link%20on%20this%20page&url=https%3A%2F%2Fbleacherreport.com%2Fac-milan"

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
        /* Main title styling */
        .main-title {
            color: #000000;
            font-family: "Times New Roman", Times, serif;
            font-size: 2.5em;
            border-bottom: 2px solid #000000;
            margin-bottom: 20px;
        }
        
        /* Category title styling */
        .category-title {
            color: #000000;
            font-family: "Times New Roman", Times, serif;
            font-size: 2em;
            margin-bottom: 15px;
        }
        
        /* Source header styling */
        .source-header {
            padding: 8px;
            margin-bottom: 15px;
            border-radius: 5px;
            background-color: #E8E8E8;
            color: #333333;
            border: 1px solid #CCCCCC;
        }
        .source-header h3 {
            font-size: 1.2em;
            font-family: "Times New Roman", Times, serif;
        }
        
        .headline-link {
            color: #1E1E1E;
            text-decoration: none;
            padding: 8px 12px;
            border-radius: 5px;
            margin: 3px 0;
            display: block;
            background-color: #FFFFFF;
            border-left: 4px solid #CCCCCC;
            transition: all 0.2s ease-in-out;
            font-size: 0.9em;
            font-family: "Times New Roman", Times, serif;
        }
        
        .headline-link:hover {
            background-color: #F5F5F5;
            border-left-color: #666666;
            padding-left: 15px;
        }
        
        .divider {
            margin: 3px 0;
            border: none;
            height: 1px;
            background-color: #CCCCCC;
        }
        
        /* Make the columns more compact */
        .stColumn {
            padding: 0.5rem !important;
            background-color: #F8F8F8;
            border-radius: 5px;
            border: 1px solid #DDDDDD;
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
                
                # Create styled headline link without showing the URL
                st.markdown(f"""
                    <a href="{link}" target="_blank" class="headline-link">
                        <strong>{item['Headline']}</strong>
                    </a>
                    <div class="divider"></div>
                """, unsafe_allow_html=True)

def display_source_headlines(source_name, source_url):
    data = fetch_headlines(source_url)
    if data:
        # Extract the base URL from the query parameter
        base_url = None
        if 'query' in data and len(data['query']) > 0:
            from_params = [q for q in data['query'] if q[0] == 'FROM']
            if from_params:
                base_url = from_params[0][1]
        
        # Remove any "Headlines" text that might be in the source_name
        display_name = source_name.replace(" Headlines", "")
        
        # Make the header clickable if we have a base URL
        header_html = f"""
            <div class="source-header">
                {f'<a href="{base_url}" target="_blank" style="text-decoration: none; color: inherit;">' if base_url else ''}
                <h3 style='margin: 0;'>{display_name}</h3>
                {f'</a>' if base_url else ''}
            </div>
        """
        st.markdown(header_html, unsafe_allow_html=True)
        display_headlines(data)

def main():
    set_custom_style()
    
    # Main title with newspaper styling
    st.markdown("""
        <h1 class='main-title' style='text-align: center;'>
            📰 Andrea's Daily Brief
        </h1>
    """, unsafe_allow_html=True)
    
    # Create sidebar with category selection
    st.sidebar.markdown("""
        <h2 style='text-align: center; color: #000000; font-family: "Times New Roman", Times, serif;'>
            Select Category
        </h2>
    """, unsafe_allow_html=True)
    
    categories = {
        "🏛️ Politics": {
            "🦊 Fox News": URLs.FOX_NEWS,
            "🌐 CNN": URLs.CNN,
            "😄 The Onion": URLs.ONION
        },
        "💻 Tech": {
            "💻 Hacker News": URLs.HACKER_NEWS,
            "🚀 TechCrunch": URLs.TECH_CRUNCH,
            "💡 VentureBeat": URLs.VENTURE_BEAT,
            "🏢 CrunchBase": URLs.CRUNCH_BASE
        },
        "⚽ Soccer": {
            "🇮🇹 Football Italia": URLs.FOOTBALL_ITALIA,
            "🏆 Milan News": URLs.MILAN
        }
    }
    
    selected_category = st.sidebar.selectbox("", list(categories.keys()))
    
    if st.sidebar.button("Fetch Headlines", key="fetch_button"):
        # Remove the word 'Headlines' from the category display
        category_display = selected_category.replace(" Headlines", "")
        st.markdown(f"""
            <h2 class='category-title' style='text-align: center;'>
                {category_display}
            </h2>
        """, unsafe_allow_html=True)
        
        sources = categories[selected_category]
        
        if selected_category == "🏛️ Politics":
            cols = st.columns(3)
            for idx, (source_name, source_url) in enumerate(sources.items()):
                with cols[idx]:
                    display_source_headlines(source_name, source_url)
                    
        elif selected_category == "💻 Tech":
            cols = st.columns(4)
            for idx, (source_name, source_url) in enumerate(sources.items()):
                with cols[idx]:
                    display_source_headlines(source_name, source_url)
                    
        elif selected_category == "⚽ Soccer":
            cols = st.columns(2)
            for idx, (source_name, source_url) in enumerate(sources.items()):
                with cols[idx]:
                    display_source_headlines(source_name, source_url)

if __name__ == "__main__":
    main()

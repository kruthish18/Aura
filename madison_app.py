import streamlit as st
import requests
import pandas as pd

# Page Config
st.set_page_config(page_title="Madison Reddit Analyzer", page_icon="🎯", layout="wide")

# --- UI Header ---
st.title('Madison Brand Intelligence')
st.markdown("### Reddit Sentiment & Trend Analysis")

# --- Sidebar ---
with st.sidebar:
    st.header("Search Settings")
    search_query = st.text_input('Brand/Topic:', value="OpenAI")
    limit = st.slider("Posts to Fetch", 5, 100, 50)
    st.divider()
    st.caption("Madison Framework v1.2")

N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/dd898add-0a6e-42ed-b336-4763a6615ca0"

if st.button('Run Analysis'):
    with st.spinner(f'Madison Agent scanning Reddit for "{search_query}"...'):
        try:
            payload = {"query": search_query, "limit": limit}
            response = requests.post(N8N_WEBHOOK_URL, json=payload)
            
            if response.status_code == 200:
                    raw_response = response.json()
                    
                    # Logic to find the list of 50 posts
                    if isinstance(raw_response, list) and len(raw_response) > 0:
                        # n8n Aggregate node usually returns [{ "data": [...] }]
                        posts = raw_response[0].get('data', raw_response)
                    elif isinstance(raw_response, dict):
                        # If it's a single dict, look for the 'data' key we made in n8n
                        posts = raw_response.get('data', [raw_response])
                    else:
                        posts = []

                    if posts:
                        df = pd.DataFrame(posts)
                        
                        # Fix upvotes to be numbers
                        df['Upvotes'] = pd.to_numeric(df['Upvotes'], errors='coerce').fillna(0).astype(int)
                        
                        st.success(f"Madison found {len(df)} results!")

                        # Metrics Section
                        m1, m2, m3 = st.columns(3)
                        m1.metric("Total Mentions", len(df))
                        m2.metric("Highest Upvotes", df['Upvotes'].max())
                        m3.metric("Avg Engagement", int(df['Upvotes'].mean()))

                        # Table Section
                        st.subheader("📊 Brand Mentions")
                        st.dataframe(df[['Post Title', 'Upvotes', 'User', 'URL']], use_container_width=True)

                        # Detailed Content Section
                        st.subheader("📝 Deep Dive")
                        for i, row in df.iterrows():
                            with st.expander(f"{row['Post Title']}"):
                                st.write(row['Bodytexts'])
                                st.markdown(f"[Link to Post]({row['URL']})")
                    else:
                        st.warning("Connected to n8n, but no posts were found in the data.")
        except Exception as e:
            st.error(f"UI Error: {e}")
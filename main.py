import streamlit as st
from util import *

# Page title of the application
page_title = "YouAsk"
page_icon = "🎬"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout="wide")

if "video_details" not in st.session_state:
    st.session_state["video_details"] = []

# Application Title and description
st.title(f'{page_title}{page_icon}')
st.write('***:blue[The YouTube Companion You Never Knew You Needed]***')
st.write("""
Ever watched a YouTube video and wished you could just ask it questions live? YouAsk lets you paste any YouTube video 
URL, instantly fetches the video details (title, thumbnail, views, likes), and lets you fire away questions about the 
content. Whether it’s a tech tutorial, history lesson, or cooking hack — we’ll help you understand better. 🚀

Features:
* 🔍 Instant Video Insights
* ❓ Smart Q&A Engine
* 📽️ Supports All YouTube Video Types
* 🧠 Learn More, Watch Smarter!
""")
# Display footer in the sidebar
display_footer()

st.subheader('YouTube Video URL', divider='gray')
yt_url = st.text_input('Enter YouTube Video URL', max_chars=100, label_visibility="collapsed", placeholder='YouTube Video URL')
button = st.button("Process", type='primary', disabled=not yt_url)

if button:
    with st.spinner('Processing ...', show_time=True):
        video_id = extract_video_id(yt_url)
        yt_df, thumbnail = get_video_details(video_id, st.secrets['YT_API_KEY'])
        st.session_state["video_details"].append({'video_insights': yt_df, 'thumbnail': thumbnail})
        st.success('Video has been processed Successfully', icon=":material/check_circle:")

if st.session_state["video_details"]:
    col1, col2 = st.columns([.7, .3], gap='large')
    with col1:
        st.subheader('Video Insights:📊')
        st.dataframe(st.session_state["video_details"][-1]['video_insights'], hide_index=True)
    with col2:
        st.subheader('Video Thumbnail:🖼️')
        st.image(st.session_state["video_details"][-1]['thumbnail'])





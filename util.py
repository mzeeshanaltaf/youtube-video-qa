import streamlit as st
import pandas as pd
import re
from googleapiclient.discovery import build
from datetime import datetime


def extract_video_id(url):
    """Extract video ID from YouTube URL."""
    # Matches typical YouTube URLs
    regex = r'(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|embed|shorts)\/|\S*[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(regex, url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")


def get_video_details(video_id, api_key):
    """Fetch video details using YouTube Data API."""
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.videos().list(
        part='snippet,statistics',
        id=video_id
    )

    response = request.execute()

    if not response['items']:
        raise Exception("Video not found or invalid video ID.")

    video = response['items'][0]

    snippet = video['snippet']
    statistics = video.get('statistics', {})

    published_at = datetime.strptime(snippet['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d')
    views_count = f'{int(statistics.get('viewCount', 'N/A')):,}'
    likes_count = f'{int(statistics.get('likeCount', 'N/A')):,}'
    comments_count = statistics.get('commentCount', 'N/A')
    if comments_count != 'N/A':
        comments_count = f'{int(comments_count):,}'

    thumbnail = snippet['thumbnails']['high']['url']

    yt_df = {'Info': ['Channel Name', 'Video Title', 'Published', 'Views', 'Likes', 'Comments'],
             'Details': [snippet['channelTitle'],
                         snippet['title'],
                         published_at,
                         views_count,
                         likes_count,
                         comments_count],
             }

    return pd.DataFrame(yt_df), thumbnail

def display_footer():
    footer = """
    <style>
    /* Ensures the footer stays at the bottom of the sidebar */
    [data-testid="stSidebar"] > div: nth-child(3) {
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
    }

    .footer {
        color: grey;
        font-size: 15px;
        text-align: center;
        background-color: transparent;
    }
    </style>
    <div class="footer">
    Made with ❤️ by <a href="mailto:zeeshan.altaf@gmail.com">Zeeshan</a>.
    </div>
    """
    st.sidebar.markdown(footer, unsafe_allow_html=True)
import streamlit as st
from src import reddit

st.write(
    """
# Reddit problem finder

Hello *world!*

This is a simple app that uses OpenAI's GPT-4 to summarize and interpret Reddit posts and comments. It uses it to summarize and suggest software solutions to the problems in the posts. 

It is basically a brainstorming tool for entrepreneurs without imagination, a tool I personally very much needed.

Tabs guide:

- **Specific post**: Enter a link to a specific Reddit post and see the summary and interpreted summary.
- **Hot, New, Top, Rising**: Enter a subreddit name and see the summary and interpreted summary of the top post. (e.g. "learnprogramming")
"""
)


def render_post(post):
    st.header("Original Post:")
    st.markdown(f"https://www.reddit.com{post['permalink']}")

    st.header("Title:")
    st.markdown(post["selftext"])

    st.header("Summary:")
    st.markdown(post["summary"])

    st.header("Interpreted Summary:")
    st.markdown(post["interpret_summary"])


tab1, tab2, tab3, tab4, tab5 = st.tabs(["Specific post", "Hot", "New", "Top", "Rising"])

# SPECIFIC POST
with tab1:
    redditurl = st.text_input("Link to reddit post", "")

    specific_with_comments = st.checkbox(
        "With comments", value=False, key="specific_with_comments"
    )

    if redditurl.startswith("https://www.reddit.com/"):
        post = reddit.get_specific_post(redditurl, specific_with_comments)

        render_post(post)

# HOT POSTS
with tab2:
    subreddit = st.text_input("Name of subreddit", "", key="hot_posts_subreddit")

    with_comments = st.checkbox("With comments", value=False, key="hot_with_comments")

    if subreddit:
        posts = reddit.get_hot_posts(subreddit, 1, with_comments)

        for post in posts:
            render_post(post)

# NEW POSTS
with tab3:
    subreddit = st.text_input("Name of subreddit", "", key="new_posts_subreddit")

    with_comments = st.checkbox("With comments", value=False, key="new_with_comments")

    if subreddit:
        posts = reddit.get_new_posts(subreddit, 1, with_comments)

        for post in posts:
            render_post(post)

# TOP POSTS
with tab4:
    subreddit = st.text_input("Name of subreddit", "", key="top_posts_subreddit")

    with_comments = st.checkbox("With comments", value=False, key="top_with_comments")

    time_filter = st.selectbox(
        "Time filter",
        [
            "hour",
            "day",
            "week",
            "month",
            "year",
            "all",
        ],
    )

    if subreddit:
        posts = reddit.get_top_posts(subreddit, 1, time_filter, with_comments)

        for post in posts:
            render_post(post)

# RISING POSTS
with tab5:
    subreddit = st.text_input("Name of subreddit", "", key="rising_posts_subreddit")

    with_comments = st.checkbox(
        "With comments", value=False, key="rising_with_comments"
    )

    if subreddit:
        posts = reddit.get_rising_posts(subreddit, 1, with_comments)

        for post in posts:
            render_post(post)

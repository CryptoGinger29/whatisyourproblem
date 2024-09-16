import streamlit as st
from src import reddit
import time

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


tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["Specific post", "Hot", "New", "Top", "Rising", "Persona chat"]
)

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


def streamreponse(response: str):

    for word in response.split():
        yield word + " "
        time.sleep(0.05)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


with tab6:
    problem = st.text_input("What is the problem?")
    age = st.text_input("What is your personas age?")
    gender = st.text_input("What is your personas gender?")

    if problem and age and gender:
        st.title("Your persona chat")
        messages = st.container(height=500)

        prompt = st.chat_input("Get personal with your persona")
        with messages:
            # Accept user input
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if prompt:
                # Display user message in chat message container
                st.session_state.messages.append({"role": "user", "content": prompt})

                with st.chat_message("user"):
                    st.markdown(prompt)

                response = reddit.chat(
                    problem, age, gender, st.session_state.messages, prompt
                )
                # Display response in chat message container
                with st.chat_message("assistant"):
                    st.write_stream(streamreponse(response))

                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )

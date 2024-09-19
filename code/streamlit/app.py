import streamlit as st
from src import reddit
import time
from streamlit_navigation_bar import st_navbar

styles = {
    "nav": {
        "background-color": "rgb(0, 0, 0)",
    },
    "div": {
        "max-width": "48rem",
    },
    "span": {
        "border-radius": "0.5rem",
        "color": "rgb(255, 255, 255)",
        "margin": "0 0.125rem",
        "padding": "0.4375rem 0.625rem",
    },
    "active": {
        "background-color": "rgba(255, 255, 255, 0.25)",
    },
    "hover": {
        "background-color": "rgba(255, 255, 255, 0.35)",
    },
}

page = st_navbar(
    ["Home", "Opportunity", "User", "Problem", "Solution", "Feedback", "Contact"],
    styles=styles,
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


def streamreponse(response: str):

    for word in response.split():
        yield word + " "
        time.sleep(0.05)


if page == "Home":
    st.write(
        """
    # Reddit problem finder
    """
    )
    container = st.container(border=True)
    container.write(
        """
    Hello *world!*

    This is a simple app that uses OpenAI's GPT-4 to summarize and interpret Reddit posts and comments. It uses it to summarize and suggest software solutions to the problems in the posts. 

    It is basically a brainstorming tool for entrepreneurs without imagination, a tool I personally very much needed.

    The app has 4 main features (inspired by the 4 main questions of the [unstuck map](https://unstuckmap.com/) by Nikkel Blaase):
    -   Do you understand the opportunity? - Use the Reddit screen to find a problem
    -   Do you understand the user?
    -   Do you understand the problem?
    -   Do you know how to solve the problem?

    There should be a flow from opportunity -> user -> problem -> solution.

    The features should work in unity to help you understand the problem and find a solution. The app is still in development and is so far just a way for me to play with some cool tech, and if it creates value for you that's just a large extra plus.

    """
    )
elif page == "Opportunity":
    st.write(
        """
    Find your opportunity by using the Reddit screener to find a problem. 

    Finding a opportunity is linked to understanding the problem and the user, however when starting with the opportunity we try to play the numbers game and find a problem that is common and has a lot of potential users. Hence the screener.

    Tabs guide:

    - **Specific post**: Enter a link to a specific Reddit post and see the summary and interpreted summary.
    - **Hot, New, Top, Rising**: Enter a subreddit name and see the summary and interpreted summary of the top post. (e.g. "learnprogramming")
    """
    )
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Specific post", "Hot", "New", "Top", "Rising"]
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

        with_comments = st.checkbox(
            "With comments", value=False, key="hot_with_comments"
        )

        if subreddit:
            posts = reddit.get_hot_posts(subreddit, 1, with_comments)

            for post in posts:
                render_post(post)

    # NEW POSTS
    with tab3:
        subreddit = st.text_input("Name of subreddit", "", key="new_posts_subreddit")

        with_comments = st.checkbox(
            "With comments", value=False, key="new_with_comments"
        )

        if subreddit:
            posts = reddit.get_new_posts(subreddit, 1, with_comments)

            for post in posts:
                render_post(post)

    # TOP POSTS
    with tab4:
        subreddit = st.text_input("Name of subreddit", "", key="top_posts_subreddit")

        with_comments = st.checkbox(
            "With comments", value=False, key="top_with_comments"
        )

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
elif page == "User":
    st.write(
        """
    Get to know your user better by chatting with a persona.

    This is a way to conduct synthetic user research, which ofcourse isn't a substitue for real user research. You can enter a problem

    **Persona chat**: Enter a age, gender and a short description of the persona and have a chat with a persona to understand the potential user better.
    """
    )
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    age = st.text_input("What is your personas age?")
    gender = st.text_input("What is your personas gender?")
    description = st.text_area("What is your personas description?")

    if description and age and gender:
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
                    description, age, gender, st.session_state.messages, prompt
                )
                # Display response in chat message container
                with st.chat_message("assistant"):
                    st.write_stream(streamreponse(response))

                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
elif page == "Problem":
    st.write(
        """
    # Problem

    This is the problem page, and a place to understand the problem better. This is a tool to help you create a problem hypothesis and understand the problem better.

    """
    )

    st.write(
        """
        TBD
        """
    )

elif page == "Solution":
    st.write(
        """
    # Solution

    This is the solution page

    """
    )
    st.write(
        """
        TBD
        """
    )


elif page == "Feedback":
    st.write(
        """
    # Feedback

    Hello there! If you have any feedback, please let us know below.

    """
    )
    with st.form(key="feedback_form"):
        contact = st.text_input("Contact")
        feedback = st.text_area("Feedback")
        submit = st.form_submit_button("Submit")
        if submit:
            st.write("Thank you for your feedback!")
elif page == "Contact":
    st.write(
        """
    # Contact

    Find me on reddit at [u/KingGinger29](https://www.reddit.com/user/KingGinger29/)

    """
    )

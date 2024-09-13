import praw
import os
from dotenv import load_dotenv
from openai import OpenAI
from .setup_logging import logger

load_dotenv()

r = praw.Reddit(
    client_id=os.environ["reddit_client_id"],
    client_secret=os.environ["reddit_client_secret"],
    user_agent=os.environ["reddit_user_agent"],
)

client = OpenAI()


def interpret(text: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a creative and curious assistant, that is deeply interested in finding out what peoples problems are and solving them using software solutions in the style of Pieter Levels. When ever a text is parsed to you, you will try to understand the text and suggest three seperate MVP solutions including 3 features to their problem that they can build.",
            },
            {
                "role": "user",
                "content": text,
            },
        ],
    )

    return completion.choices[0].message.content


def summarize_gpt3(text: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a expert in summarizing text. What ever length of input you receive you will summarize it to a length of 100 characters.",
            },
            {"role": "user", "content": text},
        ],
    )

    return completion.choices[0].message.content


def summarize(
    text: str,
    max_length_input: int = 512,
    max_chunks: int = 1,
) -> str:

    # separate the input text from the summarization task
    chunk_texts_ls = [
        text[i : i + max_length_input] for i in range(0, len(text), max_length_input)
    ]

    logger.info(f"Number of total chunks: {len(chunk_texts_ls)}")

    chunk_texts_ls = chunk_texts_ls[:max_chunks]

    ls_summary = []
    for text_chunk in chunk_texts_ls:
        summary = summarize_gpt3(text_chunk)
        ls_summary.append(summary)

    summary = "\n \n".join(ls_summary)

    return summary


def handle_post(post, with_comments=False):
    obj = {
        "title": post.title,
        "url": post.url,
        "permalink": post.permalink,
        "score": post.score,
        "num_comments": post.num_comments,
        "created": post.created_utc,
        "selftext": post.selftext,
    }

    complete_string = obj["title"] + obj["selftext"] + ". "

    if with_comments:
        post.comments.replace_more(limit=0)
        comments = post.comments.list()
        ls_comments = []
        for comment in comments:
            ls_comments.append(
                {
                    "body": comment.body,
                    "score": comment.score,
                    "created": comment.created_utc,
                }
            )

            complete_string += f"{comment.body}. \n "

        obj["comments"] = ls_comments

    summary = summarize(complete_string)

    obj["summary"] = summary
    interpret_summary = interpret(summary)

    obj["interpret_summary"] = interpret_summary

    return obj


def get_specific_post(url: str, with_comments: bool = False):
    post = r.submission(url=url)
    obj = handle_post(post, with_comments)

    return obj


def get_hot_posts(subreddit: str, limit: int, with_comments: bool = False):
    page = r.subreddit(subreddit)
    top_posts = page.hot(
        limit=limit,
    )

    ls_posts = []
    for post in top_posts:
        obj = handle_post(post, with_comments)
        ls_posts.append(obj)

    return ls_posts


def get_new_posts(subreddit: str, limit: int, with_comments: bool = False):
    page = r.subreddit(subreddit)
    top_posts = page.new(
        limit=limit,
    )

    ls_posts = []
    for post in top_posts:
        obj = handle_post(post, with_comments)
        ls_posts.append(obj)

    return ls_posts


def get_rising_posts(subreddit: str, limit: int, with_comments: bool = False):
    page = r.subreddit(subreddit)
    top_posts = page.rising(
        limit=limit,
    )

    ls_posts = []
    for post in top_posts:
        obj = handle_post(post, with_comments)
        ls_posts.append(obj)

    return ls_posts


def get_top_posts(
    subreddit: str, limit: int, time_filter: str = "all", with_comments: bool = False
):
    page = r.subreddit(subreddit)
    top_posts = page.top(
        limit=limit,
        time_filter=time_filter,
    )

    ls_posts = []
    for post in top_posts:
        obj = handle_post(post, with_comments)
        ls_posts.append(obj)

    return ls_posts

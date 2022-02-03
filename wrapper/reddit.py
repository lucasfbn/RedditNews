import praw


class Reddit:

    def __init__(self, subreddit, client_id, client_secret, user_agent, username, password):
        self.subreddit = subreddit
        self.api = praw.Reddit(client_id=client_id,
                               client_secret=client_secret,
                               user_agent=user_agent,
                               username=username,
                               password=password)

    def submit(self, title, url):
        self.api.subreddit(self.subreddit).submit(title, url=url)

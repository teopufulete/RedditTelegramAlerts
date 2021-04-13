from __future__ import unicode_literals
import telegram as tg
import praw
import logging
import json
from time import sleep
from datetime import datetime


with open("./info.txt",'r') as f:
    credentials = f.read().split(',')

client_id, client_secret , reddit_username, reddit_password, token, chat_id = [credentials[i] for i in (0,1,2,3,4,5)]


class RedditAlerts:
    def __init__(self, client_id, client_secret, reddit_username, reddit_password):
         self.client_id = client_id
         self.client_secret = client_secret
         self.reddit_username = reddit_username
         self.reddit_password = reddit_password
         self.is_logged_in = False
         

    def login(self):
        self.reddit = praw.Reddit(user_agent="telegram keeb watcher",
                        client_id=self.client_id,
                        client_secret=self.client_secret,
                        username=self.reddit_username,
                        password=self.reddit_password)
        reddit.read_only = True
        self.is_logged_in = True
        print('Login?', self.is_logged_in)


    def prev_submissions(self):
            try:
                with open('prev_sub', 'r') as f:
                    return f.read().strip()
            except:
                return None


    def write_submissions(self, curr_id):
        try:
            with open('prev_sub', 'w') as f:
                f.write(curr_id)
        except:
            print("Error writing sub ID!")


    def search_sub(self, subreddit = '', query = ''):
        reddit = self.reddit
        subreddit = reddit.subreddit(subreddit)

        self.start_time = datetime.utcnow().timestamp()
        last_sub_id = self.prev_submissions()

        post = False
        if not last_sub_id:
            print("Latest submission not found, starting all submissions!")
            post = True
        else:
            print("Last posted submission is {}".format(last_sub_id))

        while True:
            try:
                for submission in subreddit.hot():
                # for submission in subreddit.search(query):    ,'flair:"selling"', time_filter = 'day'
                    try:
                        link = "https://redd.it/{id}".format(id=submission.id)
                        
                        if not post and submission.created_utc < self.start_time:
                            print("Skipping {} --- latest submission not found!".format(submission.id))

                            if submission.id == last_sub_id:
                                post = False
                            continue
                        
                        template = "{title}\n{url}"
                        message = template.format(title=submission.title, url=submission.url)
                        print("Posting {}".format(link))

                        telegram = TelegramMessages(token, chat_id)    
                        telegram.send_message(message)

                        self.write_submissions(submission.id)
                        sleep(5)

                    except Exception as e:
                        print("Error parsing {}".format(link))

            except Exception as e:
                print("Error fetching new submissions, restarting in 10 secs")
                sleep(10)


class TelegramMessages:
    def __init__(self, token, chat_id):
        self.token = token 
        self.chat_id = chat_id              

    def send_message(self, text):
        self.bot = tg.Bot(token = token)
        bot = self.bot  
        bot.sendMessage(chat_id = chat_id, text = text)   


reddit = RedditAlerts(client_id, client_secret, reddit_username, reddit_password)
reddit.login()
reddit.prev_submissions()
reddit.search_sub('keebwatchers', 'tangerines')


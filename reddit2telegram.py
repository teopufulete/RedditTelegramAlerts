from telegram.ext import Updater, CommandHandler
import praw
import logging


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


    def search_sub(self, subreddit = '', query = ''):
        reddit = self.reddit
        subreddit = reddit.subreddit(subreddit)
    
        for submission in subreddit.search(query, time_filter = 'day'):
            return(submission.title, submission.url)
            # post_dict[submission.id] = submission.url, submission.title
            # print(post_dict)
          
          
reddit = RedditAlerts(client_id, client_secret, reddit_username, reddit_password)
reddit.login()
message = reddit.search_sub('mechmarket', 'tangerine')


class TelegramMessages:
    def __init__(self, token, telegram_channel):
        self.token = token 
        self.telegram_channel = telegram_channel      
    
    def send_message(self, text):
        self.bot = tg.Bot(token = token)
        bot = self.bot  
        bot.sendMessage(chat_id = chat_id, text = text)   

telegram = TelegramMessages(token, chat_id)
telegram.send_message(message)

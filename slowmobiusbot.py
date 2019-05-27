import os
import praw
from praw.exceptions import APIException
import traceback
import shutil
import re
import hashlib
import redis
import prawcore
import time
import mysecret
from helper import s2b
from scrapeVideo import search_download_vid




#TODO: login to reddit
#TODO: obtain job
#TODO: Retrieve Video
#TODO: Slow Video Down
#TODO: Post Video

#################
# Constants

working_path = os.path.abspath("data/working")
#user_agent =


reddit = praw.Reddit(username=mysecret.username,
                    password=mysecret.password,
                    client_id=mysecret.client_id,
                    user_agent="slowmobiusbot v0.1")

dryrun = s2b(os.getenv('DRYRUN'), True)
debug = s2b(os.getenv('DEBUG'), False)
include_old_mentions = s2b(os.getenv('INCLUDE_OLD_MENTIONS'), False)
sleep_time_s = 10

me = reddit.user.me().name
message_submission_name = "replies_from_" + me


r = redis.Redis(
    host='redis',
    port=6379,
    password='')


# post the
def post_reply(reply_md, mention):
    print("post_reply... ")
    if dryrun:
        print("reply would be:" + reply_md)
        return

    for i in range(0, 5):

        try:
            mention.reply(reply_md)
            return

        except prawcore.exceptions.RequestException:
            print("RequestException... Trying again...")

        except APIException as e:
            if e.error_type == 'RATELIMIT':
                print("I was posting too fast. Error-Message: " + e.message)
                wait_time_m = int(re.search(r'\d+', e.message).group()) + 1

                if wait_time_m > 10:
                    wait_time_m = 10
                print("Going to sleep for " + str(wait_time_m) + " minutes.")
                time.sleep(wait_time_m * 60)
            else:
                raise e
    print("post_reply... failed")



def send_message(mention, text):
    text = "pinging /u/" + mention.author.name + "\n\n" + text
    if dryrun:
        print("message would be: " + text)
        return

    #s = get_message_submission(assume_over_18(mention))
    print("replying...")
    #s.reply(text)




# generates the string that will be replyed in the comment
# Contains the address with the slowed gif
def create_reply(uploaded_url, proc_time, upload_time, over_18, cashe_hit):
    nsfw_note = "----------NSFW--------- \n\n" if over_18 else ""

    #if ""





def get_next_job():
    for mention in reddit.inbox.mentions(limit=50):
        if not mention.new and not include_old_mentions:
            continue
        if not dryrun:
            mention.mark_read()
        else:
            print("dryrun: " + str(dryrun))

        return mention




def working_main():
    pass


def clear_env():
    if os.path.exists(working_path):
        shutil.rmtree(working_path)
    os.makedirs(working_path)
    os.chdir(working_path)


def assume_over_18(mention):
    pass


def main():

    print("Starting...")

    while True:

        reply_md = ""

        try:

            clear_env()

            mention = get_next_job()

            if mention is None:
                time.sleep(sleep_time_s)
                continue

            print("submission: " + mention.submission.id + " - " + mention.submission.shortlink)
            over_18 = assume_over_18(mention)

            start_time = time.time()

            #input_path = search_download_vid(mention.submission, user_agent)
        finally:


            print("Finish")








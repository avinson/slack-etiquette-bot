import slack
import time
from django.core.management.base import BaseCommand
from django.conf import settings
from slackbot.models import User

class ShameBot:

    GUIDE_URL = 'https://hiverhq.com/blog/slack-etiquette/'

    def __init__(self, region='us-west-2'):
        self.username = "ur_friend"
        self.icon_emoji = ":robot_face:"
        self.timestamp = ""
        self.web_client = ""
        self.rtm_client = ""

    def parse_message(self, text, user, channel, ts):
        if 'Hello' in text:
            self.web_client.chat_postMessage(
                channel=channel,
                text=f"Hi <@{user}>!"
            )

        if '@here' in text:
            self.web_client.chat_postMessage(
                channel=channel,
                text=f"Hi <@{user}>, I noticed you used @here."
            )

bot = ShameBot()

@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    data = payload['data']
    bot.web_client = payload['web_client']
    bot.rtm_client = payload['rtm_client']
    if all(k in data for k in ("text","user")):
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']
        bot.parse_message(text=data['text'],user=user,channel=channel_id,ts=thread_ts)

class Command(BaseCommand):
    help = 'Starts the bot for the first'

    def handle(self, *args, **options):
        rtm_client = slack.RTMClient(token=settings.SLACK_API_TOKEN)
        rtm_client.start()

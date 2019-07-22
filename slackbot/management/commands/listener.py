import logging
import slack
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from slackbot.models import Slackuser, Message

class EtiquetteBot:

    def __init__(self, region='us-west-2'):
        self.username = "ur_friend"
        self.icon_emoji = ":robot_face:"
        self.web_client = ""
        self.rtm_client = ""

    def parse_message(self, text, user, channel, ts):
        dt = datetime.utcfromtimestamp(int(float(ts)))
        if 'Hello' in text:
            self.web_client.chat_postMessage(
                channel=channel,
                text=f"Hi <@{user}>!"
            )

        if '<!here>' in text or '<!channel>' in text:
            first_time = False
            if Slackuser.objects.filter(username=user).exists():
                s = Slackuser.objects.filter(username=user).first()
            else:
                first_time = True
                s = Slackuser(username=user)
                s.save()
            m = Message(slackuser=s, text=text, dt=dt, channel=channel)
            m.save()

            if first_time:
                self.web_client.chat_postMessage(
                    channel=user,
                    as_user=True,
                    text=f"Hi <@{user}> " + settings.INITIAL_TEXT
                )

            # get the most recent message
            #latest = Message.objects.filter(slackuser=s).order_by('-dt').first()
            #logger.error(f"last is: {latest.dt}")

            # if s.last_reminder > REMIND_THRESHOLD, send settings.REMIND_TEXT

            # if > PRIVATE_NAG_THRESHOLD for 7 days, channel=user
            #self.web_client.chat_postMessage(
            #    channel=user,
            #    as_user=True,
            #    text=f"Hi <@{user}> " + settings.PRIVATE_NAG_TEXT
            #)

            # if > PUBLIC_NAG_THRESHOLD for 7 days, channel=channel
            #self.web_client.chat_postMessage(
            #    channel=channel,
            #    as_user=True,
            #    text=f"Hi <@{user}> " + settings.PUBLIC_NAG_TEXT
            #)

logger = logging.getLogger(__name__)
bot = EtiquetteBot()

@slack.RTMClient.run_on(event='message')
def receive_message(**payload):
    data = payload['data']
    #logger.error(f"payload is: {data}")
    bot.web_client = payload['web_client']
    bot.rtm_client = payload['rtm_client']
    if all(k in data for k in ("text","user")):
        channel = data['channel']
        thread_ts = data['ts']
        user = data['user']
        bot.parse_message(text=data['text'],user=user,channel=channel,ts=thread_ts)

class Command(BaseCommand):
    help = 'Starts the bot for the first'

    def handle(self, *args, **options):
        rtm_client = slack.RTMClient(token=settings.SLACK_API_TOKEN)
        rtm_client.start()

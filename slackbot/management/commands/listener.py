import logging
import time
import slack
from datetime import datetime, timedelta
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
        if '<!here>' in text or '<!channel>' in text:
            dt = datetime.utcfromtimestamp(int(float(ts)))
            first_time = False
            if Slackuser.objects.filter(username=user).exists():
                s = Slackuser.objects.filter(username=user).first()
            else:
                first_time = True
                s = Slackuser(username=user)
                s.save()
            m = Message(slackuser=s, text=text, dt=dt, channel=channel)
            m.save()

            last_week = datetime.now() - timedelta(days=7)
            abuses = Message.objects.filter(slackuser=s, dt__gte=last_week).count()

            #remind_diff = int(time.time() - datetime.timestamp(s.last_reminder))
            #logger.error(f"remind_diff is {remind_diff}")

            if first_time:
                self.web_client.chat_postMessage(
                    channel=user,
                    as_user=True,
                    text=f"Hi <@{user}> " + settings.INITIAL_TEXT
                )
                logger.error(f"Sent {user} initial text on {dt}")

            # does the user need reminding?
            elif int(time.time() - datetime.timestamp(s.last_reminder)) > int(settings.REMIND_THRESHOLD * 86400):
                s.last_reminder = timezone.now()
                s.save()
                self.web_client.chat_postMessage(
                    channel=user,
                    as_user=True,
                    text=f"Hi <@{user}> " + settings.REMIND_TEXT
                )
                logger.info(f"Sent {user} reminder on {dt}")
            # count the number of abuses in the last week
            elif abuses > int(settings.PUBLIC_NAG_THRESHOLD):
                    # only nag once per day
                    if int(time.time() - datetime.timestamp(s.last_public_nag)) > 86400:
                        s.last_public_nag = timezone.now()
                        s.save()
                        self.web_client.chat_postMessage(
                            channel=channel,
                            as_user=True,
                            text=f"Hi <@{user}> :wave: You've used `@here` or `@channel` {abuses} times in the last week. That's a lot! Next time, consider giving your message a few minutes without the tag before tagging a large group (and maybe tag specific people!). :slightly_smiling_face:"
                        )
                        logger.error(f"Sent {user} public nag on {dt}")
            # now check for a private nag
            elif abuses > int(settings.PRIVATE_NAG_THRESHOLD):
                    # only nag once per day
                    if int(time.time() - datetime.timestamp(s.last_private_nag)) > 86400:
                        s.last_private_nag = timezone.now()
                        s.save()
                        self.web_client.chat_postMessage(
                            channel=user,
                            as_user=True,
                            text=f"Hi <@{user}> :wave: You've used `@here` or `@channel` {abuses} times in the last week. Please review the guidelines at {settings.GUIDE_URL} and consider giving your message a few minutes without the tag before tagging a large group (and maybe tag specific people!). :slightly_smiling_face:"
                        )
                        logger.error(f"Sent {user} private nag on {dt}")


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

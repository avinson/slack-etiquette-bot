import os
import slack
from shame import ShameBot

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
        bot.parse_message(text=data['text'],user=user,channel=channel_id)

def main():
    slack_token = os.environ["SLACK_API_TOKEN"]
    rtm_client = slack.RTMClient(token=slack_token)
    rtm_client.start()

main()

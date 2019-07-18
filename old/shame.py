import boto3

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

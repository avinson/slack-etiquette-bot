import boto3

class ShameBot:

    GUIDE_URL = 'https://hiverhq.com/blog/slack-etiquette/'

    def __init__(self, dynamo_table='slack-abuse', region='us-west-2'):
        self.username = "ur_friend"
        self.icon_emoji = ":robot_face:"
        self.timestamp = ""
        self.web_client = ""
        self.rtm_client = ""

        dynamodb = boto3.resource('dynamodb', region_name=region, endpoint_url='http://localhost:8000')
        self.table = dynamodb.Table(dynamo_table)

    def parse_message(self, text, user, channel):
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

FROM python:3.7-alpine



# gcc needed for slackclient
RUN apk add --no-cache build-base libffi-dev

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

## defaults for settings.py
# the etiquette guide to send to users
ENV GUIDE_URL https://get.slack.help/hc/en-us/articles/202009646-Notify-a-channel-or-workspace
# default django secret key
ENV SECRET_KEY 2#g(+&igmrw57&ij6r-gzvu8lo7pze78(x)-#ox)#%uo9lf4hy
# channel size below which the bot will not enforce / remind about etiquette
ENV CHANNEL_MEMBER_THRESHOLD 20
# number of days after which to remind the user when they use @channel or @here
ENV REMIND_THRESHOLD 30
# number of uses per week after which a user is sent a DM with a more nagging message to reduce their usage of @here/@channel
ENV PRIVATE_NAG_THRESHOLD 5
# number of uses per week after which a user is responded to publicly in the channel, actively shaming them to knock it off
ENV PUBLIC_NAG_THRESHOLD 10
# misc
ENV DJANGO_ENV development
ENV MYSQL_ENABLED no

COPY . .

WORKDIR /usr/src/app



CMD ["python", "manage.py", "listener"]

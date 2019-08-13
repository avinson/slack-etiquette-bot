# slack-etiquette-bot

## Overview

Slack bot to reduce abuse of `@here`s and `@channel`s at your company. Edit `slackbot/settings.py` to adjust the messages that are sent. This may eventually be moved to environment variables.

## Env Vars

### Optional
* `GUIDE_URL` -- URL to send to users once (with periodic reminders) with guidelines. (Defaults to `https://get.slack.help/hc/en-us/articles/202009646-Notify-a-channel-or-workspace`)
* `CHANNEL_MEMBER_THRESHOLD` -- Don't enforce on channels below this threshold (Defaults to `20`)
* `REMIND_THRESHOLD` -- Resend the `GUIDE_URL` and overview message after this many days (Defaults to `30`)
* `PRIVATE_NAG_THRESHOLD` -- Send the user a DM with a sterner warning if they use `@here/@channel` this many times per week (Defaults to `6`)
* `PUBLIC_NAG_THRESHOLD` -- Begin publicly shaming the user in the channel they posted after this many abuses per week (Defaults to `10`)
* `EBOT_MYSQL_ENABLED` -- Enable the mysql backend. Defaults to sqlite.
* `EBOT_MYSQL_HOST` -- Mysql host endpoint
* `EBOT_MYSQL_PASS`
* `EBOT_MYSQL_PORT`
* `EBOT_MYSQL_USER`

### Required
* SLACK_API_TOKEN


## Usage

To use locally, set the required missing environment variables (e.g. `SLACK_API_TOKEN`) and create/migrate the db:
```
$ python manage.py migrate
$ python manage.py makemigrations slackbot
$ python manage.py migrate
```

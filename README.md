# slack-etiquette-bot

## Overview

Slack bot to reduce abuse of `@here`s and `@channel`s via shaming. Edit `slackbot/settings.py` to adjust the messages that are sent. This may eventually be moved to environment variables.

### Initial Message

The bot initially messages a user with the following, sends a reminder every 30 days and finally begins first privately and then publicly (in the channel where the abuse occurs) shaming the user for abuse.

---

:wave: I'm your friendly slack etiquette bot. Since you used `@here` or `@channel` in a channel with more than 20 members, I'm passing along some guidelines here: https://get.slack.help/hc/en-us/articles/202009646-Notify-a-channel-or-workspace

Please review the guidelines and consider avoiding the use of `@here` or `@channel` when possible as this can be disruptive or annoying to other employees.
Here are some examples of when using these keywords is *not appropriate*:
* There exists leftover food in the kitchen.
* There will exist food in the kitchen sometime in the future (this is not timely enough to warrant disrupting workflow).
* You brought back some treats from your trip (thank you for your kindness but people can read scrollback for this).
* You forgot something of low value in a conference room (again, people can read the scrollback and answer your question eventually).

Thanks for reading over this and being considerate. I'll send out another friendly reminder every 30 days. Cheers!


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
* `SLACK_API_TOKEN`


## Usage

To use locally, set the required missing environment variables (e.g. `SLACK_API_TOKEN`) and create/migrate the db:
```
$ python manage.py migrate
$ python manage.py makemigrations slackbot
$ python manage.py migrate
```

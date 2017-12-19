import slackweb
from datetime import datetime

class SlackUtils:

    def __init__(self):
        self.slack = slackweb.Slack(url="https://hooks.slack.com/services/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")

    def info(self, message, channel='notify'):
        notification = "[{application}][{datetime}]:INFO| {message}".format(datetime=datetime.now(), message=message)
        self.slack.notify(text=notification, channel=channel)

    def danger(self, message, channel='notify'):
        notification = "[{datetime}]:Danger| {message}".format(datetime=datetime.now(), message=message)
        self.slack.notify(text=notification, channel=channel)

    def warn(self, message, channel='notify'):
        notification = "[{datetime}]:Warn| {message}".format(datetime=datetime.now(), message=message)
        self.slack.notify(text=notification, channel=channel)

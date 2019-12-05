import json
import os
from slack import WebClient
import websocket
from slacker import Slacker
from flask import Flask, request, make_response,Response
from httplib2 import Http
import requests
import time
import re

token = "xoxb-644338026258-845515840694-3UjEanEpA0TWJM9a9nLNOVSX"
slack_client = WebClient(os.environ.get(token))
# events = [{'type': XXX, 'text': YYY, 'user': ZZZ}, ...]
#slack.chat.post_message('#test', 'I have a question')
#app = Flask(__name__)
# instantiate Slack client
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "calculate"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    values = (matches.group(1), matches.group(2),matches.group(3),matches.group(4).strip())
    return (values)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")

#def get_answer():
   #return "HEllO"

#def event_handler(event_type, slack_event):
    #if event_type == "app_mention" and "message" :

        #channel = slack_event["event"]["channel"]

        #text = get_answer()

        #slack.chat.post_message(channel, text)

        #return make_response("앱 멘션 메시지가 보내졌습니다.", 200, )

    #message = "[%s] 이벤트 핸들러를 찾을 수 없습니다." % event_type

    #return make_response(message, 200, {"X-Slack-No-Retry": 1})

#@app.route("/slack", methods=["GET", "POST"])
#def hears():
    #slack_event = json.loads(request.data)

    #if "challenge" in slack_event:
        #return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})

    #if "event" in slack_event:
       # event_type = slack_event["event"]["type"]

       # return event_handler(event_type, slack_event)

    #return make_response("슬랙 요청에 이벤트가 없습니다.", 404, {"X-Slack-No-Retry": 1})

#@app.route('/webhook', methods = ['GET'])
#def saving():
    #if "message" in slack_event:
        #return

#if __name__ == '__main__':
     #app.run('0.0.0.0', port=8080)

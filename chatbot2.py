import json
from slacker import Slacker
from flask import Flask, request, make_response
from slack import RTMClient
import os

token  = "xoxb-644338026258-845515840694-3UjEanEpA0TWJM9a9nLNOVSX"

slack = Slacker(token)

app = Flask(__name__)


def get_answer():

    return "안녕하세요."


# 이벤트 핸들하는 함수

def event_handler(event_type, slack_event):

    if event_type == "app_mention" and "message":

        channel = slack_event["event"]["channel"]


        text = get_answer()

        slack.chat.post_message(channel, text)

        return make_response("앱 멘션 메시지가 보내졌습니다.", 200, )

    message = "[%s] 이벤트 핸들러를 찾을 수 없습니다." % event_type

    return make_response(message, 200, {"X-Slack-No-Retry": 1})

@RTMClient.run_on(event= "message")

def say_hello(**paylaod) :
    data = paylaod['data']
    web_client = paylaod['web_client']
    if 'calculate' in data['text'] :
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']

        web_client.chat_postMessage(
            channel=channel_id,
            text= f"Hi <@(user)>!",
            thread_ts = thread_ts
        )
rtm_client = RTMClient(
    token=token,
    connect_method='rtm.start'
)
rtm_client.start()

@app.route("/slack", methods=["GET", "POST"])

def hears():

    slack_event = json.loads(request.data)

    if "challenge" in slack_event:

        return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})

    if "event" in slack_event:

        event_type = slack_event["event"]["type"]

        return event_handler(event_type, slack_event)

    return make_response("슬랙 요청에 이벤트가 없습니다.", 404, {"X-Slack-No-Retry": 1})


@app.route('/slack', methods=['POST'])
def inbound():
    if request.form.get('token') == env.SLACK_WEBHOOK_SECRET:
        channel = request.form.get('channel_name')
        # 누가 말했는지
        username = request.form.get('user_name')
        text = request.form.get('text')
        if "@U6JN34THT" in text:
            slack.chat.post_message(channel, attachments=attachments_json)
if __name__ == '__main__':

    app.run('0.0.0.0', port=8080)



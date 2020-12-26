import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["init",
            "add", "astart", "aend", "aact", "atag", 
            "show", "schedule", "statisic", 
            "change",
            "cact", "act1", "act2", 
            "ctime", "tstart", "tend", "tact", 
            "ctag", "gact", "gtag"],
    transitions=[
        {
            "trigger": "advance",
            "source": "init",
            "dest": "add",
            "conditions": "is_going_to_add",
        },
        {
            "trigger": "advance",
            "source": "add",
            "dest": "astart",
            "conditions": "is_going_to_astart",
        },
        {
            "trigger": "advance",
            "source": "astart",
            "dest": "aend",
            "conditions": "is_going_to_aend",
        },
        {
            "trigger": "advance",
            "source": "aend",
            "dest": "aact",
            "conditions": "is_going_to_aact",
        },
        {
            "trigger": "advance",
            "source": "init",
            "dest": "show",
            "conditions": "is_going_to_show",
        },
        {
            "trigger": "advance",
            "source": "show",
            "dest": "schedule",
            "conditions": "is_going_to_schedule",
        },
        {
            "trigger": "advance",
            "source": "show",
            "dest": "statistic",
            "conditions": "is_going_to_statistic",
        },
        {
            "trigger": "advance",
            "source": "init",
            "dest": "change",
            "conditions": "is_going_to_change",
        },
        {
            "trigger": "advance",
            "source": "change",
            "dest": "cact",
            "conditions": "is_going_to_cact",
        },
        {
            "trigger": "advance",
            "source": "cact",
            "dest": "act1",
            "conditions": "is_going_to_act1",
        },
        {
            "trigger": "advance",
            "source": "act1",
            "dest": "act2",
            "conditions": "is_going_to_act2",
        },
        {
            "trigger": "advance",
            "source": "change",
            "dest": "ctime",
            "conditions": "is_going_to_ctime",
        },
        {
            "trigger": "advance",
            "source": "ctime",
            "dest": "tact",
            "conditions": "is_going_to_tact",
        },
        {
            "trigger": "advance",
            "source": "tact",
            "dest": "tstart",
            "conditions": "is_going_to_tstart",
        },
        {
            "trigger": "advance",
            "source": "tstart",
            "dest": "tend",
            "conditions": "is_going_to_tend",
        },
        {
            "trigger": "advance",
            "source": "change",
            "dest": "ctag",
            "conditions": "is_going_to_ctag",
        },
        {
            "trigger": "advance",
            "source": "ctag",
            "dest": "gact",
            "conditions": "is_going_to_gact",
        },
        {
            "trigger": "advance",
            "source": "gact",
            "dest": "gtag",
            "conditions": "is_going_to_gtag",
        },
        {
            "trigger": "advance",
            "source": ["atag", "schedule", "statisic", "act2", "tend", "gtag"],
            "dest": "init",
            "conditions": "is_going_to_init",
        }
    ],
    initial="init",
    auto_transitions=False,
    show_conditions=True,
)
"""
machine = TocMachine(
    states=["user", "state1", "state2"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state1",
            "conditions": "is_going_to_state1",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state2",
            "conditions": "is_going_to_state2",
        },
        {"trigger": "go_back", "source": ["state1", "state2"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)
"""

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

@app.route('/', methods=['GET'])
def home():
    return "hi, my first chatbot!"

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text), False)

    return "OK"


@app.route('/webhook', methods=['POST'])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route('/show-fsm', methods=['POST'])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")

if __name__ == "__main__":
    #port = os.environ.get("PORT", 8000)
    port = os.environ['PORT']
    #port = os.environ['PORT']
    app.run(host="0.0.0.0", port=port, debug=True)

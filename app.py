from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('13kDmLwf0sr9E96PTlfLnmb7cMu405G1bqHLj+/N1DVofe8WkEKNVWR7C1Bzi1H9ok6O0KdVImuPlAM0zU0terB96MnE6H0gIwfe/pseADTWzZ55Fc9d1vkrWMdHzqamGaraUQqLfvpRwCT+ELsWggdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f8c35a5e48243aa631cbc6a7cca9487f')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    s = '你吃飯了嗎?'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text= s))


if __name__ == "__main__":
    app.run()
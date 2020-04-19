from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,StickerSendMessage, LocationSendMessage
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
    r = '很抱歉, 您說什麼'

    if'給我貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='11537',
            sticker_id='52002734'
        )
        

        line_bot_api.reply_message(
        event.reply_token,
        sticker_message)
        return

    if '我現在在哪' in msg:
        location_message = LocationSendMessage(
        title='你的位置',
        address='Singapore',
        latitude=1.290270,
        longitude=103.851959
        )

        line_bot_api.reply_message(
        event.reply_token,
        location_message)
        return

    if msg in ['hi', 'Hi']:
        r = '嗨'
    elif msg =='你吃飯了嗎':
        r = '還沒'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '訂位' in msg:
        r = '您想訂位, 是嗎?'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text= r))


if __name__ == "__main__":
    app.run()
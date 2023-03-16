import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import config
import re
from UserList import userList
import RegexPattern as reg

# ボットトークンとソケットモードハンドラーを使ってアプリを初期化します
app = App(token=config.SLACK_BOT_TOKEN)

@app.message(reg.MRPattern)
def requestReview(message):
    # print(message)
    if re.match(reg.userPattern, message['text']):
        response = createResponse(message)
        reply(message, response)

def createResponse(message):
    response = ""
    userName = re.split("[\(\)]", message['text'])[1]
    if userName in userList:
        for userId in userList.values():
            if userId != message['user']:
                response += f"<@{userId}> "
        response += "レビューお願いします"
    return response
        
def reply(message, response):
    app.client.chat_postMessage(
            text=response,
            channel=message['channel'],
            thread_ts=message['ts']
        )
# アプリを起動します
if __name__ == "__main__":
    SocketModeHandler(app, config.SLACK_APP_TOKEN).start()
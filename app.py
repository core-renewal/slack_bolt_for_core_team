from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import config
import re
from UserList import userList
import RegexPattern as reg

# ボットトークンとソケットモードハンドラーを使ってアプリを初期化します
app = App(token=config.SLACK_BOT_TOKEN,
          signing_secret=config.SLACK_SIGNING_SECRET)

@app.message(reg.MR_PATTERN)
def requestReview(message):
    if message['channel'] == config.TARGET_CHANNEL_ID:
        response = createResponse(message)
        reply(message, response)

def createResponse(message):
    response = ""
    gitName = re.split("[\(\)]", message['text'])[1]
    if gitName in userList:
        for name in userList:
            if name != gitName:
                response += f"<@{userList[name]}> "
        response += "レビューお願いします"
    return response
        
def reply(message, response):
    app.client.chat_postMessage(
            text=response,
            channel=config.TARGET_CHANNEL_ID,
            thread_ts=message['ts']
        )
    
@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)
    
# アプリを起動します
if __name__ == "__main__":
    # SocketModeHandler(app, config.SLACK_APP_TOKEN).start()
    app.start(port=3000)
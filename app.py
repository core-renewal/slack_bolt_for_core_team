from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import config
import re
from UserList import userList
import RegexPattern as reg
from ReplyMessage import ReplyMessage

# ボットトークンとソケットモードハンドラーを使ってアプリを初期化します
# app = App(token=config.SLACK_BOT_TOKEN)
app = App(token=config.SLACK_BOT_TOKEN,
          signing_secret=config.SLACK_SIGNING_SECRET)

CACHED_TS = ""

@app.message(reg.MR_PATTERN)
def requestReview(message):
    global CACHED_TS
    print(message)
    validate(message)
    if (
        re.match(reg.DRAFT_WIP, message['text'], re.IGNORECASE) 
        or re.match(reg.DRAFT_RC, message['text'], re.IGNORECASE) 
        or re.match(reg.DRAFT_PBI, message['text'], re.IGNORECASE)
    ):
        return
    
    response = reviewResponse(message)
    if response.mention != "":
        reply(message['ts'], response.createResponse())
        
@app.message(reg.MR_COMMENT)
def mention(message):
    commentContent = message['attachments'][0]
    print(commentContent)
    validate(message)
    
    response = gitMention(commentContent)
    if response.mention != "":
        reply(message['ts'], response.createResponse())

def reviewResponse(message):
    gitName = re.split(reg.SPLIT_ID, message['text'])[1]
    if gitName not in userList:
        return ""
    res = ReplyMessage("", "レビューお願いします。")
    for name in userList:
        if name != gitName:
            res.addMention(name)
    return res

def gitMention(message):
    matchResult = re.compile(reg.MENTIONED_IDS).finditer(message['text'])
    res = ReplyMessage("","MRでメンションされました。")
    for name in matchResult:
        gitName = name.group(1)
        if gitName in userList:
            res.addMention(gitName)
    return res

def reply(ts, response):
    app.client.chat_postMessage(
            text=response,
            channel=config.TARGET_CHANNEL_ID,
            thread_ts=ts
        )
    
def validate(message):
    global CACHED_TS
    if message['ts'] == CACHED_TS:
        return
    CACHED_TS = message['ts']
    if message['channel'] != config.TARGET_CHANNEL_ID:
        return
    
@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)
    
# アプリを起動します
if __name__ == "__main__":
    print("app activated!")
    # SocketModeHandler(app, config.SLACK_APP_TOKEN).start()
    app.start(port=3000)

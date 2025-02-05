from UserList import userList

class ReplyMessage:
    mention = ""
    message = ""
    
    def addMention(self, name):
        self.mention += f"<@{userList[name]}> "
        
    def addMessage(self, text):
        message += text
    
    def createResponse(self):
        return self.mention + self.message
    
    def __init__(self, mention, message):
        self.mention = mention
        self.message = message
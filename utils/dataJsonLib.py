import json
from models.User import User
import os

class dataJSON:
    
    def __init__(self, path):
        self.path = path
        
        file = None
        if not os.path.exists("users.json"):
            file = open("users.json", "w")
        else:
            file = open("users.json", "r+")
            
        if os.path.getsize("users.json") == 0:
            file.write(json.dumps({"users":{}}))
        
        file.close()
    
    def hasCredentials(self, chat_id):
        json_line = json.loads(open(self.path, "r").read())
        for i in json_line["users"]:
            if int(json_line["users"][i]["chat_id"]) == chat_id:
                if json_line["users"][i]["user_info"]["username"] != "" and json_line["users"][i]["user_info"]["password"] != "":
                    return True
        return False

    def isNewUser(self, chat_id):
        json_line = json.loads(open(self.path, "r").read())
        for i in json_line["users"]:
            if int(json_line["users"][i]["chat_id"]) == chat_id:
                return False
        return True

    def saveNewUser(self, chat_id, username):
        json_line = json.loads(open(self.path, "r").read())
        if (len(json_line["users"]) == 0):
            json_line["users"]['0'] = (User(chat_id, username, "").parseJson())
        elif (len(json_line["users"]) > 0):
            json_line["users"][str(int(json_line["users"][-1]) + 1)] = (User(chat_id, username, "").parseJson())
        open(self.path, "w").write(json.dumps(json_line))

    def getUserUsername(self, chat_id):
        json_line = json.loads(open(self.path, "r").read())
        for i in json_line["users"]:
            if int(json_line["users"][i]["chat_id"]) == chat_id:
                return json_line["users"][i]["user_info"]["username"]
        return ""
    
    def getUserPassword(self, chat_id):
        json_line = json.loads(open(self.path, "r").read())
        for i in json_line["users"]:
            if int(json_line["users"][i]["chat_id"]) == chat_id:
                return json_line["users"][i]["user_info"]["password"]
        return ""

    def setUserPassword(self, chat_id, password):
        json_line = json.loads(open(self.path, "r").read())
        for i in json_line["users"]:
            if int(json_line["users"][i]["chat_id"]) == chat_id:
                json_line["users"][i]["user_info"]["password"] = password
                open(self.path, "w").write(json.dumps(json_line))
                return

    def setUserUsername(self, chat_id, username):
        json_line = json.loads(open(self.path, "r").read())
        for i in json_line["users"]:
            if int(json_line["users"][i]["chat_id"]) == chat_id:
                json_line["users"][i]["user_info"]["username"] = username
                open(self.path, "w").write(json.dumps(json_line))
                return

    def setUserStatus(self, chat_id, status):
        json_line = json.loads(open(self.path, "r").read())
        for i in json_line["users"]:
            if int(json_line["users"][i]["chat_id"]) == chat_id:
                json_line["users"][i]["user_info"]["status"] = status
                open(self.path, "w").write(json.dumps(json_line))
                return

    def getUserStatus(self, chat_id):
        json_line = json.loads(open(self.path, "r").read())
        for i in json_line["users"]:
            if int(json_line["users"][i]["chat_id"]) == chat_id:
                return json_line["users"][i]["user_info"]["status"]
        return ""

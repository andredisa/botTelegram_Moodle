import requests
import re
from bs4 import BeautifulSoup

class Contact:
    def __init__(self, username, chatId, userId, timestamp):
        self.username = username
        self.chatId = chatId
        self.userId = userId
        self.timestamp = timestamp
    
    def __str__(self):
        return f"Username: {self.username} -> UserId: {self.userId}"

class MoodleLib:
    # costruttore
    def __init__(self, username, password):
        username = username.strip()
        if ("_" in username):
            self.username = username
            first_name = username.split("_")[0][0].upper()+username.split("_")[0][1:]
            last_name = username.split("_")[1][0].upper()+username.split("_")[1][1:]
            
            self.chatUserName = first_name+" "+last_name
        elif "." in username:
            self.username = username
            first_name = username.split(".")[0][0].upper()+username.split(".")[0][1:]
            last_name = username.split(".")[1][0].upper()+username.split(".")[1][1:]
            self.chatUserName = first_name+" "+last_name
        else:
            return print("Username non valido")
        self.password = password
        self.req = requests.Session()
        self.sesskey = ""
        self.MyUserId = ""
        self.contacts = []

    def isLogged(self):
        url = "https://agora.ismonnet.it/agora415/my/"
        res = self.req.get(url, allow_redirects=True)
        soup = BeautifulSoup(res.text, features='html.parser')
        if "Login" in soup.select("title")[0].text:
            return False
        return True

    def login(self):
        url = 'https://agora.ismonnet.it/agora415/login/index.php'
        res = self.req.post(url, allow_redirects=True)
        soup = BeautifulSoup(res.text, features='html.parser')
        token = soup.select("input[name='logintoken']")[0]['value']
        res = self.req.post(url, data={
            'logintoken': token,
            'username': self.username,
            'password': self.password
        }, allow_redirects=True)
        
        if ("Login errato, riprova" in res.text) or res.status_code != 200:
            return "Login fallito"
        
        url = "https://agora.ismonnet.it/agora415/my/"
        res = self.req.get(url, allow_redirects=True)
        
        soup = BeautifulSoup(res.text, features='html.parser')
        
        self.MyUserId = soup.select("footer[id='page-footer']")[0].select("div[class='logininfo']")[0].select("a")[0]['href'].split("=")[1]
        self.sesskey = soup.select("footer[id='page-footer']")[0].select("div[class='logininfo']")[0].select("a")[1]['href'].split("=")[1]
        
        return "Login effettuato con successo"

    def HomePage(self, req):
        url = 'https://agora.ismonnet.it/agora415/?redirect=0'
        res = req.get(url, allow_redirects=True)
        soup = BeautifulSoup(res.text, features='html.parser')
        return soup

    def getCourses(self, req):
        soup = self.HomePage(req)
        corsi = soup.select("div[id='frontpage-course-list']")[0].select("div.card.dashboard-card")
        
        courses = ""
        for corso in corsi:
            nome = corso.select("div.course-category")[0].text.strip() + ':\n\t'
            nome += corso.select("a.aalink.coursename.mr-2.mb-1")[0].text.strip() + ': '
            
            link = corso.select("a")[0]['href'].strip() + '\n'
            s = str(nome) + str(link) + '\n'
            courses += s

        return courses
        
    def getChatInfoJson(self):
        
        url = f"https://agora.ismonnet.it/agora415/lib/ajax/service.php?sesskey={self.sesskey}&info=core_message_get_conversations"
        json = [
            {
                "index":0,
                "methodname":"core_message_get_conversations",
                "args": {
                    "userid":self.MyUserId,
                    "type":1,
                    "limitnum":51,
                    "limitfrom":0,
                    "favourites":False,
                    "mergeself":True
                }
            }
        ]
        
        res = self.req.post(url, json=json, allow_redirects=True)
        
        return res.json()
    
    def getChatName(self):
        self.contacts = []
        json = self.getChatInfoJson()
        
        conversations = json[0]['data']['conversations']
        
        for conv in conversations:
            members = conv['members']
            fullname = members[0]['fullname']
            self.contacts.append(Contact(fullname, int(conv['id']), int(members[0]['id']), int(conv['messages'][0]['timecreated'])))
        
        result = []
        for user in self.contacts:
            result.append(user.username)
        
        return result
    
    def getChatOf(self, name):
        contact = self.getContact(name)
        
        url = f"https://agora.ismonnet.it/agora415/lib/ajax/service.php?sesskey={self.sesskey}&info=core_message_get_conversation_messages"
        
        json = [
            {
                "index":0,
                "methodname":"core_message_get_conversation_messages",
                "args": {
                    "currentuserid":self.MyUserId,
                    "convid":contact.chatId,
                    "newest":True,
                    "limitnum":101,
                    "limitfrom":1
                }
            }
        ]
        
        res = self.req.post(url, json=json, allow_redirects=True)
        messages = []
        members = []
            
        if len(res.json()[0]['data']['messages']) > 0:
            messages = res.json()[0]['data']['messages']
            members = res.json()[0]['data']['members']
            MyUserId = (members[0]['id'] if members[0]['id'] != self.MyUserId else members[1]['id'])
        
        conversation = []
        
        for message in messages:
            message['text'] = message['text']
            message['text']= self.cleanMessage(message['text'])
            s = (self.chatUserName if message['useridfrom'] == MyUserId else contact.username)+ ": "+ message['text']
            conversation.insert(0, s)
        
        # siccome la prima richiesta dei messaggi non restituisce l'ultimo devo farne un'altra
        json = [
            {
                "index":0,
                "methodname":"core_message_get_conversation_messages",
                "args": {
                    "currentuserid":self.MyUserId,
                    "convid":contact.chatId,
                    "newest":True,
                    "limitnum":0,
                    "limitfrom":0,
                    "timefrom":contact.timestamp
                }
            }
        ]
        
        res = self.req.post(url, json=json, allow_redirects=True)
        data = res.json()[0]['data']
        text = data['messages'][0]['text']
        text = self.cleanMessage(text)
        
        lastMess = (contact.username if data['messages'][0]['useridfrom'] == contact.userId else self.chatUserName)+ ": "+ text
        
        conversation.append(lastMess)
        result = ""
        
        for message in conversation:
            result += message + "\n\n\n"
        
        return result
    
    def cleanMessage(self, message):
        result = ""
        result = re.sub(r'<img.*?>', '', message) # rimuovo le immagini
        result = re.sub(r'<span.*?>', '', result) # rimuovo i tag span
        result = re.sub(r'</span>', '', result)
        result = re.sub(r'<div.*?>', '', result) # rimuovo i tag div
        result = re.sub(r'</div>', '', result)
        result = re.sub(r'<p.*?>', '', result) # rimuovo i tag p
        result = re.sub(r'</p>', '', result)
        result = re.sub(r'<br>', '', result) # rimuovo i tag br
        result = re.sub(r'<a.*?>', '', result) # rimuovo i tag a
        result = re.sub(r'</a>', '', result)
        return result
    
    def sendMessageTo(self, name, message):
        contact = self.getContact(name)
        
        url = f"https://agora.ismonnet.it/agora415/lib/ajax/service.php?sesskey={self.sesskey}&info=core_message_send_instant_messages"
        
        text = message
        
        json = [
            {
                "index":0,
                "methodname":"core_message_send_messages_to_conversation",
                "args": {
                    "conversationid":contact.chatId,
                    "messages": [
                        {
                            "text":text
                        }
                    ]
                }
            }
        ]
        
        res = self.req.post(url, json=json, allow_redirects=True)
        
        return (True if res.status_code == 200 else False)

    def getUnreadMessages(self):
        url = f"https://agora.ismonnet.it/agora415/lib/ajax/service.php?sesskey={self.sesskey}&info=core_message_get_unread_conversations_count"
        
        json = [
            {
                "index":0,
                "methodname":"core_message_get_conversation_counts",
                "args": {
                    "userid":self.MyUserId
                }
            },
            {
                "index":1,
                "methodname":"core_message_get_unread_conversation_counts",
                "args": {
                    "userid":self.MyUserId
                }
            }
        ]
        
        res = self.req.post(url, json=json, allow_redirects=True)
        
        return res.json()[1]['data']['types']['1'] + res.json()[1]['data']['types']['2']

    def getLastMessageFrom(self, name):
        contact = self.getContact(name)
        
        url = f"https://agora.ismonnet.it/agora415/lib/ajax/service.php?sesskey={self.sesskey}&info=core_message_get_conversation_messages"
        
        # siccome la prima richiesta dei messaggi non restituisce l'ultimo devo farne un'altra
        json = [
            {
                "index":0,
                "methodname":"core_message_get_conversation_messages",
                "args": {
                    "currentuserid":self.MyUserId,
                    "convid":contact.chatId,
                    "newest":True,
                    "limitnum":0,
                    "limitfrom":0,
                    "timefrom":contact.timestamp
                }
            }
        ]
        
        res = self.req.post(url, json=json, allow_redirects=True)
        data = res.json()[0]['data']
        text = data['messages'][0]['text']
        text = self.cleanMessage(text)
        
        lastMess = (contact.username if data['messages'][0]['useridfrom'] == contact.userId else self.chatUserName)+ ": "+ text
        
        return lastMess
        
    def getContact(self, name):
        # controllo che il nome contenga uno spazio
        if (" " not in name.strip()):
            return False
        # se la lista dei nomi è vuota, la riempio
        if len(self.contacts) == 0:
            self.getChatName()
        
        # mi salvo nome e cognome dell'utente per dare la possibilità di passare
        # il nome e il cognome in qualsiasi ordine e con qualsiasi lettera maiuscola
        firstName = name.split(" ")[0].lower()
        lastName = name.split(" ")[1].lower()
        # mi salvo il nome corretto per poterlo poi stampare
        contact = Contact("", 0, 0, 0)
        
        # scorro tutti i nomi delle chat con all'interno anche l'id della chat dell'utente
        for c in self.contacts:
            if firstName in c.username.lower() and lastName in c.username.lower():
                contact = c
                break
        
        if contact.chatId == 0 and contact.username == "":
            return False
        
        return contact
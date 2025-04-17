import time
import threading
import os
from moodle.MoodleLib import MoodleLib as Moodle

stopThread = False

class TgMoodle:
    
    def __init__(self, bot):
        self.moodle = {}  # oggetto Moodle per gestire le chat
        self.bot = bot

    def startLiveChat(self, name, chat_id):
        global stopThread
        lastMsg = self.moodle[str(chat_id)].getLastMessageFrom(name)
        while True:
            result = self.moodle[str(chat_id)].getLastMessageFrom(name)
            
            if result != lastMsg and (result.split(":")[0].split(" ")[0].lower() != self.bot.json_file.getUserUsername(chat_id).split("_")[0].lower()) and (result.split(":")[0].split(" ")[1].lower() != self.bot.json_file.getUserUsername(chat_id).split("_")[1].lower()):
                # invio il messaggio in chat senza il nome del mittente
                self.bot.send_TGmessage(result[len(result.split(":")[0]) + 2:], chat_id)
                lastMsg = result
            
            if stopThread:
                stopThread = False
                return
            
            time.sleep(1)

    def tryLogin(self, username, password, chat_id):
        self.moodle[str(chat_id)] = Moodle(username, password)
        if "successo" in self.moodle[str(chat_id)].login():
            return True
        else:
            self.moodle[str(chat_id)] = None
            return False
        
    def moodleCommands(self, message, chat_id, cmdLogged, tmpDir):
        if message == "/login":
            # controllo se l'utente è già loggato
            if (str(chat_id) in self.bot.moodleTool.moodle) and self.bot.moodleTool.moodle[str(chat_id)].isLogged():
                response = "Sei già loggato! 🤩\n" + cmdLogged
                self.bot.json_file.setUserStatus(chat_id, "")
            # controllo se l'utente ha già salvato le credenziali
            elif self.bot.json_file.hasCredentials(chat_id):
                self.bot.send_TGmessage("Sto provando a loggarti con le credenziali già salvate...", chat_id)
                # se le credenziali salvate sono corrette
                if self.tryLogin(self.bot.json_file.getUserUsername(chat_id), self.bot.json_file.getUserPassword(chat_id), chat_id):
                    response = "Login effettuato con successo! 👌🏻\n" + cmdLogged
                    self.bot.json_file.setUserStatus(chat_id, "")
                else:
                    # altrimenti gliele faccio inserire nuovamente
                    self.bot.json_file.setUserStatus(chat_id, "login")
                    response = "Le credenziali salvate sono errate, inseriscile nuovamente\nInserisci il tuo username"
                
            else:
                self.bot.json_file.setUserStatus(chat_id, "login")
                response = "Inserisci il tuo username"
        
        elif self.bot.json_file.getUserStatus(chat_id).startswith("login"):
            # controllo se l'utente ha già inserito l'username e la password
            if self.bot.json_file.getUserStatus(chat_id) == "login_password":
                self.bot.json_file.setUserPassword(chat_id, message)
                self.bot.send_TGmessage("Login in corso...", chat_id)
                if self.tryLogin(self.bot.json_file.getUserUsername(chat_id), message, chat_id):
                    response = "Login effettuato con successo! 👌🏻\n" + cmdLogged
                else:
                    response = "Login fallito"
                
                self.bot.json_file.setUserStatus(chat_id, "")
            # controllo se deve inserire ancora la password
            elif self.bot.json_file.getUserStatus(chat_id) == "login":
                self.bot.json_file.setUserUsername(chat_id, message)
                self.bot.json_file.setUserStatus(chat_id, "login_password")
                response = "Inserisci la tua password"

        elif message == "/unreadmessages":
            if not (str(chat_id) in self.bot.moodleTool.moodle):
                response = "ACCESSO NEGATO! ❌\nDevi prima effettuare il login:\n/login"
                
            else:
                result = self.bot.moodleTool.moodle[str(chat_id)].getUnreadMessages()
                
                if result != None:
                    if result == 0:
                        response = "Hai già letto tutti i messaggi! 🥳"
                    elif result == 1:
                        response = "Hai 1 messaggio da leggere! 🧐\n"
                    else:
                        response = f"Hai {str(result)} messaggi non letti! 😴\n"
                    
            self.bot.json_file.setUserStatus(chat_id, "")

        elif message == "/getchat":
            if str(chat_id) in self.bot.moodleTool.moodle:
                response = "Scegli una chat:\n"
                cnt = 1
                for i in self.bot.moodleTool.moodle[str(chat_id)].getChatName():
                    response += f"/{cnt}\t" + str(i) + "\n"
                    cnt+=1
                self.bot.json_file.setUserStatus(chat_id, "getChat")
                
            else:
                response = "ACCESSO NEGATO! ❌\nDevi prima effettuare il login:\n/login"
        
        elif (self.bot.json_file.getUserStatus(chat_id) == "getChat" and message[1:].isdigit()) or (self.bot.json_file.getUserStatus(chat_id) == "" and message.startswith("/getChat") and " " in message and message.split(" ")[1].isdigit()):
            if not (str(chat_id) in self.bot.moodleTool.moodle):
                response = "ACCESSO NEGATO! ❌\nDevi prima effettuare il login:\n/login"
            
            else:
                if not message.startswith("/"):
                    response = "Devi selezionare una chat valida 😕"
                    
                else:
                    val = -1
                    if " " in message and message.split(" ")[1].isdigit():
                        val = int(message.split(" ")[1]) - 1
                    else:
                        val = int(message[1:]) - 1

                    name = self.bot.moodleTool.moodle[str(chat_id)].getChatName()[val]
                    result = self.bot.moodleTool.moodle[str(chat_id)].getChatOf(name)

                    if result:
                        tmpFile = os.path.join(tmpDir, f"MoodleChat_{name}.txt")
                        file = open(tmpFile, "w", encoding="UTF-8")
                        file.write(result)
                        file.close()
                        
                        self.bot.send_TGmessage(chat_id, open(tmpFile, "rb"), "Chat esportata con successo! 😎")
                        os.remove(tmpFile)
                        
                    else:
                        response = "La chat selezionata non è disponibile per qualche strano motivo 🤷‍♂️"
        
        elif message == "/sendmessage":
            if not (str(chat_id) in self.bot.moodleTool.moodle):
                response = "ACCESSO NEGATO! ❌\nDevi prima effettuare il login:\n/login"
                
            else:
                self.bot.json_file.setUserStatus(chat_id, "sendMessage")
                response = "Scegli una chat:\n"
                cnt = 1
                for i in self.bot.moodleTool.moodle[str(chat_id)].getChatName():
                    response += f"/{cnt}\t" + str(i) + "\n"
                    cnt+=1
                
                response += "\n\nInserisci il nome della chat a cui vuoi mandare il messaggio e a capo scrivi il messaggio da inviare. "
                response += "Esempio:\n\n<Numero(/1, /2...)>\n[Messaggio da inviare...(nel messaggio puoi andare a capo quando vuoi)]"
        
        elif self.bot.json_file.getUserStatus(chat_id) == "sendMessage":
            if not (str(chat_id) in self.bot.moodleTool.moodle):
                response = "ACCESSO NEGATO! ❌\nDevi prima effettuare il login:\n/login"
                
            else:
                if not message.startswith("/"):
                    response = "Devi selezionare una chat valida 😕"
                    
                else:
                    val = -1
                    if "\n" in message and message.split("\n")[0].replace("/", "").isdigit():
                        val = int(message.split("\n")[0][1]) - 1
                        mess = message.split("\n")[1:]
                        
                        finalMess = ""
                        for i in range(len(mess)):
                            finalMess += mess[i] + "\n"
                        
                        result = self.bot.moodleTool.moodle[str(chat_id)].sendMessageTo(self.bot.moodleTool.moodle[str(chat_id)].getChatName()[val], finalMess)
                        
                        if result != True:
                            response = "Non è stato possibile inviare il messaggio 🤷‍♂️"
                        else:
                            response = "Messaggio inviato con successo! 😁"
                    
                    else:
                        response = "Devi selezionare una chat valida o scrivere un messaggio 😱"

        elif message == "/livechat":
            if not (str(chat_id) in self.bot.moodleTool.moodle):
                response = "ACCESSO NEGATO! ❌\nDevi prima effettuare il login:\n/login"
                
            else:
                # invio la lista delle chat disponibili
                response = "Scegli con chi vuoi parlare:\n"
                cnt = 1
                for i in self.bot.moodleTool.moodle[str(chat_id)].getChatName():
                    response += f"/{cnt}\t" + str(i) + "\n"
                    cnt+=1
                    
                self.bot.json_file.setUserStatus(chat_id, "liveChat")

        elif self.bot.json_file.getUserStatus(chat_id) == "liveChat":
            if not (str(chat_id) in self.bot.moodleTool.moodle):
                response = "ACCESSO NEGATO! ❌\nDevi prima effettuare il login:\n/login"
                
            else:
                if not message.startswith("/"):
                    response = "Devi selezionare una chat valida 🤨"
                
                else:
                    val = -1
                    if " " in message and message.split(" ")[1].isdigit():
                        val = int(message.split(" ")[1]) - 1
                    else:
                        val = int(message[1:]) - 1

                    # vado a prendere l'utente in base al numero selezionato
                    name = self.bot.moodleTool.moodle[str(chat_id)].getChatName()[val]
                    result = self.bot.moodleTool.moodle[str(chat_id)].getChatOf(name)
                    resLen = len(result.split("\n\n\n"))
                    # ricavo gli ultimi 10 messaggi
                    lastTenMessages = ""
                    if resLen > 10:
                        for i in range(resLen - 11, resLen):
                            lastTenMessages += result.split("\n\n\n")[i] + "\n\n"
                    
                    if result:
                        response = "Chat iniziata con successo! 🤠\n"
                        response += f"D'ora in poi qualunque cosa scriverai verrà inviata a {name}\n Per terminare la chat scrivi /endChat\n"
                        
                        response += "\nOra verranno mostrati gli ultimi 10 messaggi della chat:\n\n"
                        self.bot.send_TGmessage(response, chat_id)
                        response = ""
                        
                        # invio gli ultimi 10 messaggi
                        for i in range(len(lastTenMessages.split("\n\n"))):
                            self.bot.send_TGmessage(lastTenMessages.split("\n\n")[i], chat_id)
                        
                        self.bot.json_file.setUserStatus(chat_id, "liveChat_" + name)
                        
                        # avvio il thread per ricevere i messaggi in tempo reale
                        thread = threading.Thread(target=self.startLiveChat, args=(name, chat_id))
                        thread.start()
                        
                    else:
                        response = "La chat selezionata non è disponibile per qualche strano motivo 🤷‍♂️"

        elif self.bot.json_file.getUserStatus(chat_id).startswith("liveChat_"):
            if not (str(chat_id) in self.bot.moodleTool.moodle):
                response = "ACCESSO NEGATO! ❌\nDevi prima effettuare il login:\n/login"
                
            else:
                if message == "/endchat":
                    global stopThread
                    stopThread = True
                    
                    self.setUserStatus(chat_id, "")
                    response = "Chat terminata con successo! 🫠"
                    
                else:
                    # invio il messaggio
                    result = self.bot.moodleTool.moodle[str(chat_id)].sendMessageTo(self.getUserStatus(chat_id)[9:], message)
                    
                    if result != True:
                        response = "Errore durante l'invio del messaggio 💀"
        else:
            response = "Comando non riconosciuto 🚫"
            
        return response

import json
import bcrypt

class User:
    def __init__(self, chat_id, username, password):
        # Assicura che chat_id sia una stringa
        self.chat_id = str(chat_id)
        
        # Controlla che username e password non siano vuoti
        if not username or not password:
            raise ValueError("Username o password non possono essere vuoti")
        
        self.username = username
        
        # Cripta la password per una gestione sicura
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        self.status = ""
        self.TGname = ""

    def setStatus(self, status):
        """
        Imposta lo stato dell'utente.
        """
        self.status = status

    def setTGname(self, name):
        """
        Imposta il nome utente Telegram dell'utente.
        """
        self.TGname = name

    def checkPassword(self, password):
        """
        Controlla se la password fornita corrisponde a quella memorizzata.
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.password)

    def parseJson(self):
        """
        Restituisce le informazioni dell'utente in formato JSON.
        """
        return json.dumps({
            "chat_id": self.chat_id,
            "user_info": {
                "username": self.username,
                "password": self.password.decode('utf-8'),  # Nota: Criptato, ma passato come stringa per JSON
                "status": self.status
            }
        })

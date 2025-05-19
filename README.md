# 📚 Telegram Bot for Moodle Integration

> A versatile and powerful Telegram bot designed to interact with Moodle, enabling seamless communication, notifications, and course management directly through Telegram.

---

## 🚀 Project Overview

This Telegram bot integrates with the [Moodle](https://moodle.org/) platform, allowing users to interact with their Moodle accounts through Telegram. It supports actions such as logging in, retrieving course information, and sending messages to Moodle users.

---

## 💡 Features

- **💬 Message Communication**: Send and receive messages between users and the bot.
- **🔑 Login Management**: Authenticate users with their Moodle credentials.
- **📚 Course Information**: Retrieve and view courses directly within Telegram.
- **📝 User Management**: Add new users, store them, and manage user statuses.

---

## 🔧 Installation

`Follow the steps below to set up the Telegram bot for your Moodle integration:`

### 1. Clone the Repository

```bash
git clone https://github.com/andredisa/botTelegram_Moodle.git
cd telegram-moodle-bot
```

### 2. Install Dependencies

`Make sure you have Python 3.7+ installed. You can install the required dependencies using pip:`

```bash
pip install -r requirements.txt
```

### 3. Set Up Your Bot Token

`Create a file called bot_token.py and insert your bot token like this:`

```bash
TOKEN = 'your-bot-token-here'
```

> Remember to add bot_token.py to your .gitignore to keep your token secure.

### 4. Run the Bot
`Run the bot with the following command:`

```bash
python main.py
```

---

## 📁 Project Structure

```bash
.
├── bot/                         # Contains files related to the Telegram bot's functionality
│   ├── __init__.py               # Marks the directory as a Python package
│   ├── TelegramBot.py           # Main logic for handling Telegram bot interactions
│   └── TelegramToMoodle.py     # Handles communication between Telegram and Moodle
├── moodle/                       # Contains the Moodle-related functionalities
│   ├── __init__.py               # Marks the directory as a Python package
│   └── MoodleLib.py             # Library for interacting with Moodle
├── models/                       # Contains models related to user data and interactions
│   ├── __init__.py               # Marks the directory as a Python package
│   └── User.py                   # User model with credentials, chat ID, and status
├── utils/                        # Contains utility libraries and helpers
│   ├── __init__.py               # Marks the directory as a Python package
│   └── dataJsonLib.py          # Manages user data in JSON format
├── config/                       # Configuration files, including bot token and settings
│   ├── __init__.py               # Marks the directory as a Python package
│   └── bot_token.py              # File containing the Telegram bot token
├── .gitignore                    # Git ignore file to exclude files from version control (e.g., token)
├── main.py                       # Entry point of the application, starts the bot and manages updates
├── README.md                     # Project documentation and setup instructions
├── requirements.txt              # File listing project dependencies
└── LICENSE                       # License information (MIT License)
```

---

## ⚡ Usage
> Once the bot is running, interact with it through the Telegram app by searching for the bot or using the provided link. Here are some of the available commands:

`start:` **Welcome message and login instructions.**

`/login:` **Log in with your Moodle credentials.**

`/getchat:` **Retrieve your Moodle messages.**

`/sendmessage:` **Send a message to a specific user in Moodle.**

`/unreadmessages:` **Check for unread messages.**

`/livechat:` **Access live chat with the bot.**

---

## 🛠️ Requirements
- Python 3.7+

- requests library

- beautifulsoup4 for parsing HTML

> Install the required Python libraries with:
```bash
pip install -r requirements.txt
```

---

## 📎 To-Do / Future Improvements

- [ ] Modularization of commands
- [ ] Web Admin Panel (Flask)
- [ ] Deploy on Docker and rewrite file paths

---

## 👥 Contributing
> We welcome contributions to this project! Here are some ways you can help:

1. **Fork the repository** and make your changes.

2. **Submit a pull request** with a clear description of your changes.

3. Report bugs or suggest features by opening an **issue**.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 About the Author

> These applications were created for **educational and demonstration purposes only**.  
I welcome your feedback, contributions, or collaboration ideas!

💬 Feel free to reach out on [GitHub](https://github.com/andredisa) or by [email](mailto:andreadisanti22@gmail.com)!

---

## ☕ Support Me

If you find my work useful and would like to support me, you can buy me a coffee! Your support helps me keep creating and improving my projects. Thank you! 😊

<a href="https://www.buymeacoffee.com/andredisa" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

---

### 🧑‍💻✨ Happy coding

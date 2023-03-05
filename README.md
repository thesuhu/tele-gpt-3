# Tele GPT-3

Telegram bot using AI GPT-3.

## Usage

Clone this repository and install these dependencies by running the following command:

```sh
pip install -r requirements.txt
```

Rename file `.env-example` to `.env` and edit the file. Paste your [OpenAI](https://platform.openai.com/account/api-keys) api key and [Telegram Bot](https://web.telegram.com) api key:

```
OPENAI_API_KEY=
TELEGRAM_BOT_API_KEY=
```

Start the bot by running this command:

```sh
python3 main.py
```

After start the bot, it will create text file `authorized_users.txt`. Put user Telegram ID if you want to restrict who can use the bot and then restart bot.

Open the Telegram app, then search your bot, click `START` button or type `/start` command to start conversation.
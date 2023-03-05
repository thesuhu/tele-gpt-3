import openai
import os
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Load environment variables from .env file
load_dotenv()

# Enable logging
# Read the LOG_FILE_PATH value from the .env file
log_file_path = os.getenv('LOG_FILE_PATH')

# Configure logging
logging.basicConfig(filename=log_file_path,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.ERROR)

# Read the API key from the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the API key for OpenAI
openai.api_key = openai_api_key

# A list of authorized user IDs
# authorized_users = [YOUR_AUTHORIZED_USER_ID1, YOUR_AUTHORIZED_USER_ID2, ...]
# If using file, fill in authorized_users.txt, and save the user IDs, one per line.
authorized_users = []


def load_authorized_users():
    # file path
    file_path = "authorized_users.txt"
    # check if the file exists
    if not os.path.exists(file_path):
        # if the file does not exist, create an empty file
        with open(file_path, "w") as f:
            f.write(os.getenv("INIT_AUTHORIZED_USERS"))
            pass

    # open file and read the content in a list
    with open(file_path, "r") as f:
        for line in f:
            authorized_users.append(int(line.strip()))
    return authorized_users

# e.g: https://platform.openai.com/examples/default-chat


def chat_Completion(texts):
    # model davinci
    # completion = openai.Completion.create(
    #     # is set to the “text-davinci-002”, which is the “most capable” GPT-3 model based on OpenAI’s documentation
    #     engine="text-davinci-003",
    #     prompt=texts,  # is set to “text”, which is a variable representing the text input to the function
    #     max_tokens=150,  # sets out the limit for the number of words to be returned
    #     # sets out how deterministic the output of the model is. A high temperature gives the model more freedom to sample outputs.
    #     temperature=0.9,
    #     top_p=1,  # sets out the distribution to select the outputs from
    #     # is parameters which penalise the model for returning outputs which appear often
    #     frequency_penalty=0,
    #     # is parameters which penalise the model for returning outputs which appear often
    #     presence_penalty=0.6,
    #     # is a list of strings which the model will stop generating text when it encounters
    #     stop=[" Human:", " AI:"]
    # )
    # message = completion.choices[0].text

    # model gpt-3.5-turbo
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        temperature=0.01,
        messages=[
            {"role": "user", "content": texts}
        ]
    )
    # print(completion)
    message = completion.choices[0].message.content.strip()
    return message


def start(update, context):
    welcome_message = "Hi, I'm a chatbot powered by OpenAI's GPT-3. How can I help you today?"
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=welcome_message)


def chat(update, context):
    try:
        user_id = update.message.from_user.id
        if user_id in authorized_users:
            texts = update.message.text
            response = chat_Completion(texts)
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=response)
        else:
            unauthorized_message = "You are not authorized to use this bot. Please contact the bot administrator for more information."
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=unauthorized_message)
    except Exception as e:
        # Log the error
        response_error_message = "An error occurred while sending a message. Please try again later."
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=response_error_message)
        logging.error("An error occurred while sending a message: %s", str(e))
        if os.getenv("ENV") == "dev":
            print("An error occurred while sending a message: %s", str(e))
        else:
            print("An error occurred while sending a message. Check the logs for more information.")


def main():
    # Load the authorized users from a text file
    authorized_users = load_authorized_users()

    # Read the Telegram Bot API key from the environment variable
    telegram_api_key = os.getenv("TELEGRAM_BOT_API_KEY")

    # Initialize the Telegram Bot Updater
    updater = Updater(token=telegram_api_key, use_context=True)
    bot = updater.dispatcher

    # Add handlers for Telegram Bot commands
    start_handler = CommandHandler("start", start)
    bot.add_handler(start_handler)

    chat_handler = MessageHandler(Filters.text, chat)
    bot.add_handler(chat_handler)

    # Start the Telegram Bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    print('Starting chatbot...')
    try:
        main()
    except Exception as e:
        # Log the error
        logging.error(
            "An error occurred while starting the chatbot: %s", str(e))
        print("An error occurred while starting the chatbot. Check the logs for more information.")

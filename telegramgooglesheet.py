import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, jsonify
import time
import logging

app = Flask(__name__)

# Initialize the Telegram bot with your API token
bot = telegram.Bot(token='YOUR_TELEGRAM_BOT_TOKEN')

# Google Sheets setup
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
spreadsheet = client.open('Your Google Spreadsheet Name')  # Replace with your Google Spreadsheet name
worksheet = spreadsheet.get_worksheet(0)

# Function to handle new messages and write them to the Google Sheet
def process_message(update, context):
    try:
        message = update.message.text
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(update.message.date))

        # Append the message and timestamp to the Google Sheet
        row = [timestamp, message]
        worksheet.insert_rows(row, 2)  # Insert new rows at the top
    except Exception as e:
        logging.error(f"Error writing to Google Sheet: {str(e)}")

# Function to handle the /start command
def start(update, context):
    update.message.reply_text("I'm now listening to messages in the Telegram group!")

@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        data = worksheet.get_all_records()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

# Initialize the Telegram bot updater
updater = Updater(token='YOUR_TELEGRAM_BOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher

# Register a message handler
message_handler = MessageHandler(Filters.text & ~Filters.command, process_message)
dispatcher.add_handler(message_handler)

# Register a /start command handler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Start the bot
updater.start_polling()

# Keep the Flask API running
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
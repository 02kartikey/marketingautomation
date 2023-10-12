import telegram
from fbchat import Client
from fbchat.models import *
import time

# Initialize the Telegram bot with your API token
bot = telegram.Bot(token='Telegraam BOT')

# Initialize the Facebook bot with your credentials
fb_client = Client("UserName","Password")

# Initialize a variable to keep track of the last processed message ID
last_processed_message_id = None

def read_and_post_message():
    global last_processed_message_id
    # Get updates from the Telegram bot
    updates = bot.get_updates()
    
    for update in updates:
        message = update.message
        # Check if the message is new (not processed before)
        if message.message_id != last_processed_message_id:
            # Extract the message text
            message_text = message.text
            
            # Post the message to the Facebook group
            fb_client.send(Message(text=message_text), thread_id='1972128943161051', thread_type=ThreadType.GROUP)
            
            # Update the last processed message ID
            last_processed_message_id = message.message_id

while True:
    read_and_post_message()
   
    time.sleep(5)  # Adjust the delay as needed

import telegram
from fbchat import Client
from fbchat.models import *
import time
import sqlite3
import schedule

# Initialize the Telegram bot with your API token
bot = telegram.Bot(token='6062076328:AAEbTpVqd9sySmaNwgyvhNGSYZ49AbTP24Y')

# Initialize the Facebook bot with your credentials
fb_client = Client("YOUR_FACEBOOK_USERNAME", "YOUR_FACEBOOK_PASSWORD")

# Create or connect to an SQLite database
conn = sqlite3.connect('posts.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS posts
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   message TEXT,
                   timestamp INTEGER)''')
conn.commit()

# Initialize the last_processed_message_id variable
last_processed_message_id = None

def read_and_save_message():
    global last_processed_message_id
    # Get updates from the Telegram bot
    updates = bot.get_updates()

    for update in updates:
        message = update.message
        # Check if the message is new (not processed before)
        if message.message_id != last_processed_message_id:
            # Extract the message text
            message_text = message.text
            
            # Save the message to the database with a timestamp
            timestamp = int(time.time())
            cursor.execute("INSERT INTO posts (message, timestamp) VALUES (?, ?)", (message_text, timestamp))
            conn.commit()
            
            # Update the last processed message ID
            last_processed_message_id = message.message_id

def post_scheduled_message():
    current_time = int(time.time())
    
    # Get the next scheduled post from the database (or immediate posts)
    cursor.execute("SELECT * FROM posts WHERE timestamp <= ? ORDER BY timestamp ASC LIMIT 1", (current_time,))
    post = cursor.fetchone()
    
    if post:
        message_text = post[1]
        
        # Post the message to the Facebook group
        fb_client.send(Message(text=message_text), thread_id='1972128943161051', thread_type=ThreadType.GROUP)
        
        # Remove the posted message from the database
        cursor.execute("DELETE FROM posts WHERE id=?", (post[0],))
        conn.commit()

# Schedule the tasks
schedule.every(10).seconds.do(read_and_save_message)
schedule.every(5).minutes.do(post_scheduled_message)

while True:
    schedule.run_pending()
    time.sleep(1)

'''///***

Certainly, let's delve into the functionality of the provided code in more depth:

1. **Initialization:**
   - The code initializes two bot clients, one for Telegram and one for Facebook, using the respective API tokens and login credentials.
   - It also sets up a connection to an SQLite database ('posts.db') to store messages and their timestamps.

2. **Database Setup:**
   - The script establishes a connection to an SQLite database and creates a table called "posts" if it doesn't already exist. This table will store the messages and their timestamps.

3. **Global Variable:**
   - The variable `last_processed_message_id` is declared as `None` initially and will be used to keep track of the last processed message in the Telegram group. It's declared as a global variable so that it can be accessed and modified within functions.

4. **`read_and_save_message` Function:**
   - This function is responsible for reading messages from the Telegram group and saving them to the database.
   - It retrieves updates from the Telegram bot and iterates through them.
   - For each new message, it checks if the message ID is different from the `last_processed_message_id`, indicating that it's a new message.
   - If it's a new message, it extracts the text of the message, records the current timestamp, inserts the message and timestamp into the database, and updates the `last_processed_message_id`.

5. **`post_scheduled_message` Function:**
   - This function is responsible for posting scheduled messages from the database to the Facebook group.
   - It retrieves the current timestamp and checks the database for the next scheduled message (or immediate posts with timestamps in the past).
   - If a scheduled message is found, it extracts the message text, posts it to the Facebook group, and removes the message from the database.

6. **Scheduling:**
   - The code uses the `schedule` library to set up recurring tasks.
   - `read_and_save_message` is scheduled to run every 10 seconds to check for new messages in the Telegram group.
   - `post_scheduled_message` is scheduled to run every 5 minutes to post scheduled messages to the Facebook group.

7. **Continuous Execution:**
   - The script enters a loop where it continuously checks and runs scheduled tasks.
   - It first checks if there are any pending tasks to run (such as reading Telegram messages or posting scheduled Facebook messages) and executes them if there are any.
   - It then sleeps for 1 second before checking again, ensuring that it doesn't consume excessive system resources.

In summary, this script automates the process of monitoring a Telegram group, saving new messages with timestamps to an SQLite database, and posting scheduled messages to a Facebook group.
It handles the tracking of processed messages to avoid duplication and runs these tasks at specified intervals using the `schedule` library.***///'''
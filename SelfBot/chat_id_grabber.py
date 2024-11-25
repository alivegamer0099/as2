import asyncio
from telegram import Bot

# Replace with your bot's token
bot_token = "7743864679:AAE4A054aV7Be32zQ68ZXSsIk8l1dajjJGo"
bot = Bot(token=bot_token)

# This will be an asynchronous function
async def get_chat_id():
    # Fetch updates asynchronously
    updates = await bot.get_updates()
    for update in updates:
        print(f"Chat ID: {update.message.chat.id}")

# Run the async function
asyncio.run(get_chat_id())

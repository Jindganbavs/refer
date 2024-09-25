import json
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Replace 'YOUR_TOKEN' with your actual bot token
TOKEN = '7466188155:AAEUyWCJmLMC5BhQ1UfPpeSKnfPxZLooza0'
JSON_FILE = 'users.json'
MAX_MESSAGE_LENGTH = 4096

def load_json():
    """Load the JSON data from the file."""
    with open(JSON_FILE, 'r') as file:
        return json.load(file)

def save_json(data):
    """Save the JSON data to the file."""
    with open(JSON_FILE, 'w') as file:
        json.dump(data, file, indent=4)

async def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Hello! Use /edit to edit the users.json file or /view to view its contents.')

async def edit(update: Update, context: CallbackContext):
    """Handle editing the users.json file."""
    if len(context.args) < 3:
        await update.message.reply_text('Usage: /edit <section> <key> <value>')
        return

    section = context.args[0]
    key = context.args[1]
    value = context.args[2]

    data = load_json()

    if section not in data:
        await update.message.reply_text(f'Section "{section}" does not exist.')
        return

    if key not in data[section]:
        await update.message.reply_text(f'Key "{key}" does not exist in section "{section}".')
        return

    data[section][key] = value
    save_json(data)

    await update.message.reply_text(f'Successfully updated {section}/{key} to {value}.')

async def view(update: Update, context: CallbackContext):
    """Send the contents of a specific section or the entire users.json as a message."""
    try:
        data = load_json()

        if len(context.args) > 0:
            section = context.args[0]

            if section == "all":
                json_data = json.dumps(data, indent=4)
            elif section in data:
                json_data = json.dumps(data[section], indent=4)
            else:
                await update.message.reply_text(f'Section "{section}" does not exist.')
                return
        else:
            json_data = json.dumps(data, indent=4)

        # Split long messages into chunks
        for i in range(0, len(json_data), MAX_MESSAGE_LENGTH):
            chunk = json_data[i:i + MAX_MESSAGE_LENGTH]
            await update.message.reply_text(f'```{chunk}```', parse_mode='MarkdownV2')

    except Exception as e:
        await update.message.reply_text(f'Error reading JSON file: {e}')

def main():
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("edit", edit))
    application.add_handler(CommandHandler("view", view))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()

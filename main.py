from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import zipfile

# Add more text-based file extensions if needed
text_extensions = [
    ".txt", ".html", ".xml", ".css", ".js", ".json", ".csv", ".log", ".md", ".yaml",
    ".ini", ".cfg", ".bat", ".sh", ".sql", ".py", ".java", ".c", ".cpp", ".rb", ".pl",
    ".php", ".asp", ".jsp", ".jsx", ".ts", ".scss", ".less", ".sass", ".coffee",
    ".htaccess", ".properties", ".r", ".lua", ".tex", ".rmd", ".yml", ".groovy",
    ".bat", ".vbs", ".cmd", ".asm", ".pde", ".f90", ".hs", ".swift", ".pl",
    ".lisp", ".clj", ".scala"
]

def start(update, context):
    update.message.reply_text("Hello! Please send me a zip file.")

def process_zip(file_path):
    file_contents = ""
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            if os.path.splitext(file_info.filename)[1] in text_extensions:
                with zip_ref.open(file_info.filename) as file:
                    file_contents += f"{file_info.filename}\n{file.read().decode('utf-8')}\n\n"
    return file_contents

def handle_document(update, context):
    file_id = update.message.document.file_id
    file = context.bot.get_file(file_id)
    file_path = file.download()

    if file_path.endswith('.zip'):
        contents = process_zip(file_path)
        if contents:
            with open('text_contents.txt', 'w', encoding='utf-8') as txt_file:
                txt_file.write(contents)
            update.message.reply_document(open('text_contents.txt', 'rb'))
        else:
            update.message.reply_text("No text-based files found in the zip.")
    else:
        update.message.reply_text("Please send a zip file.")

def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    updater = Updater(token='6618564239:AAFocGP8FrjZCRQ3U4ur0vaV5IORfpQq-cA', use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document, handle_document))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

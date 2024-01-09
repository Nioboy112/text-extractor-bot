from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import zipfile
import os

ALLOWED_EXTENSIONS = [
    ".txt", ".csv", ".html", ".xml", ".json", ".log", ".css", ".sql", ".md", ".ini",
    ".cfg", ".bat", ".sh", ".php", ".js", ".py", ".c", ".cpp", ".java", ".rb", ".perl",
    ".pl", ".swift", ".go", ".kotlin", ".asm", ".diff", ".patch", ".tex", ".r", ".sass",
    ".scss", ".yaml", ".yml", ".htaccess", ".jsx", ".tsx", ".dart", ".vue", ".groovy",
    ".coffee", ".h", ".hh", ".m", ".f", ".fortran", ".as", ".cs", ".lisp", ".awk",
    ".asm", ".cc", ".hpp", ".hh", ".f90", ".scala", ".ts", ".gql", ".graphql", ".cob",
    ".cobol", ".ada", ".ada95", ".adb", ".ads", ".tcl", ".bat", ".bash", ".bsh", ".csh",
    ".fish", ".ksh", ".tcsh", ".zsh", ".fish", ".ps1", ".ps", ".raku", ".rs", ".psm1",
    ".pyw", ".pl", ".pm", ".rkt", ".sc", ".scm", ".ss", ".sls", ".smali", ".tsv", ".url",
    ".vbs", ".vba", ".wsf", ".xlsx", ".xls", ".xlsm", ".docx", ".doc", ".rtf"
]

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send me a zip file.')

def extract_zip(file_path: str) -> None:
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall('extracted_folder')

def send_text_content_recursive(update: Update, directory: str) -> None:
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_extension = os.path.splitext(file)[1]
            if file_extension in ALLOWED_EXTENSIONS:
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    # Send filename as a heading
                    update.message.reply_text(f"ð {file}\n\n")
                    
                    # Send text content back to user
                    for line in f:
                        update.message.reply_text(line)

def copy_text_files(update: Update, context: CallbackContext) -> None:
    file_id = update.message.document.file_id
    file = context.bot.get_file(file_id)
    file_path = file.file_path
    file.download('received_zip.zip')
    
    try:
        extract_zip('received_zip.zip')
        send_text_content_recursive(update, 'extracted_folder')
    except Exception as e:
        update.message.reply_text(f"An error occurred: {str(e)}")

def main() -> None:
    updater = Updater("6618564239:AAFocGP8FrjZCRQ3U4ur0vaV5IORfpQq-cA")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document.file_extension('zip'), copy_text_files))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

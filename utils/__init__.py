import os
from pathlib import Path
from utils.logger import Logger
from utils.helpers import *
from dotenv import load_dotenv

root_dir = Path(__file__).parent.absolute().parent
print("root_dir: ", root_dir)

pdf_dir = os.path.join(root_dir, "pdf")
os.makedirs(pdf_dir, exist_ok=True)

log_dir = os.path.join(root_dir, "logs")
os.makedirs(log_dir, exist_ok=True)

load_dotenv()

logger_handler = Logger(log_file_name="pdf_slack_bot.log", log_file_dir=log_dir)
logger = logger_handler.create_time_rotating_log(when="day", backup_count=10, name="pdf_slack_bot")

configs = {
    'root_dir': root_dir,
    'pdf_dir': pdf_dir,
    'logger': logger
}

configs = DotDict(configs)

__all__ = ['configs']

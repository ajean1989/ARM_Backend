import logging
from logging.handlers import RotatingFileHandler
import os

# Définition de la taille maximale du fichier journal
max_log_size = 20 * 1024 * 1024  # 10 Mo

log = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8')
log.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s : %(filename)s:%(lineno)s - %(levelname)s >>> %(message)s'))
file_handler = RotatingFileHandler(os.path.join("app","log",f"api-backend.log"), maxBytes=max_log_size, backupCount=5)
file_handler.setFormatter(logging.Formatter('%(asctime)s : %(filename)s:%(lineno)s - %(levelname)s >>> %(message)s'))
log.addHandler(console_handler)   
log.addHandler(file_handler)

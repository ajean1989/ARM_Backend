import logging
import os

log = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8')
log.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s : %(filename)s:%(lineno)s - %(levelname)s >>> %(message)s'))
file_handler = logging.FileHandler(os.path.join("app","log",f"api-backend.log"))
file_handler.setFormatter(logging.Formatter('%(asctime)s : %(filename)s:%(lineno)s - %(levelname)s >>> %(message)s'))
log.addHandler(console_handler)   
log.addHandler(file_handler)

import logging

class Logg : 
    def __init__(self) -> None:
        pass

    def set_log_api_backend(self):
        log = logging.getLogger("log-starter-debug")
        log.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        file_handler = logging.FileHandler("../log/api_backend-debug.log")
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        log.addHandler(console_handler)   
        log.addHandler(file_handler)
        return  log
    
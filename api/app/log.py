import logging
import os

class Logg : 
    def __init__(self) -> None:
        pass

    def set_log_api_backend_debug(self):
        log_api_ia_debug = logging.getLogger("log-api-ia-debug")
        log_api_ia_debug.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        file_handler = logging.FileHandler(os.path.join("app","log","api-backend-debug.log"))
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        log_api_ia_debug.addHandler(console_handler)   
        log_api_ia_debug.addHandler(file_handler)
        return  log_api_ia_debug
    
    def set_log_api_backend_info(self):
        log_api_ia_info = logging.getLogger("log-api-ia-info")
        log_api_ia_info.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        file_handler = logging.FileHandler(os.path.join("app","log","api-backend-info.log"))
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        log_api_ia_info.addHandler(console_handler)   
        log_api_ia_info.addHandler(file_handler)
        return  log_api_ia_info

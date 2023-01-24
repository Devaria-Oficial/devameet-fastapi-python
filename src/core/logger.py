import logging

from .config import get_settings

class ApiLogger(logging.Logger):
    def __init__(self, name = 'root'):
        super().__init__(name)

        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        
        self.addHandler(handler)
        self.setLevel(self._get_log_level())

    def _get_log_level(self):
        level = get_settings().log_level

        if level == 'debug':
            return logging.DEBUG
        elif level == 'info':
            return logging.INFO
        elif level == 'warning':
            return logging.WARNING
        elif level == 'error':
            return logging.ERROR
        elif level == 'critical':
            return logging.CRITICAL
        else:
            return logging.INFO
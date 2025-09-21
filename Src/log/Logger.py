from datetime import datetime

class Logger:
    @staticmethod
    def log(message):
        print(f"[Time]:{datetime.now()}\n[LOG] {message}")

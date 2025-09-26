from datetime import datetime

class Logger:
    @staticmethod
    def log(message):
        line = f"[Time]: {datetime.now()}\t[LOG]: {message}"
        print(line)
        with open("log.txt", "a") as f:
            f.write(f"{line}\n")

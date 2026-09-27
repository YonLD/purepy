class Finding:
    def __init__(self, level: str, message: str):
        self.level = level
        self.message = message

    @staticmethod
    def error(message: str) -> "Finding":
        return Finding("error", message)

    @staticmethod
    def warning(message: str) -> "Finding":
        return Finding("warning", message)

    @staticmethod
    def info(message: str) -> "Finding":
        return Finding("info", message)

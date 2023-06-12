
class Status:
    status: str
    filename: str
    timestamp: str
    explanation: str

    def __init__(self, json_data):
        self.status = ""
        self.filename = ""
        self.timestamp = ""
        self.explanation = ""

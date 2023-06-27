import json


class Status:
    """
    This class represents the status of the explanation
    """

    status: str
    filename: str
    timestamp: str
    explanation: str

    def __init__(self, json_data: json) -> None:
        my_data = dict(json_data)
        self.status = my_data['status']
        self.filename = my_data['filename']
        self.timestamp = my_data['timestamp']
        self.explanation = my_data['explanation']

    def is_done(self) -> bool:
        """
        This function checks if the status is done
        :return: True if the status is done, False otherwise
        """
        if self.status == 'done':
            return True
        return False

    def is_not_found(self) -> bool:
        """
        This function checks if the status is not found
        :return: True if the status is not found, False otherwise
        """
        if self.status == 'not found':
            return True
        return False

    def get_explanation(self) -> str:
        """
        This function returns the explanation
        """
        return self.explanation

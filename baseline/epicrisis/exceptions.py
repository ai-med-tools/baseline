from typing import List


class EmptyError(Exception):
    def __init__(self, message: str):
        self.message = f"EssayError: {message}"


class NotHasRequiredFieldError(Exception):
    def __init__(self, message: str):
        self.message = f"EssayError: {message}"


class FileIsExistError(Exception):
    def __init__(self):
        self.message = 'FileError: File is exist or already set'


class ValidationError(Exception):
    def __init__(self, error_list: List[str]):
        self.message = f"ValidationException: {error_list}"


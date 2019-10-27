from exceptions.http_status import HttpStatusModel
from exceptions.exception_type import ExceptionType


class ApiException(Exception):
    
    def __init__(self,
                 name: str,
                 code: str,
                 logging_message: str,
                 response_message: str,
                 http_status: HttpStatusModel,
                 type: ExceptionType):
        self.name = name
        self.code = code
        self.logging_message = logging_message
        self.public_message = response_message
        self.http_status = http_status
        self.type = type
        self.logging_messages = []
        self.external_messages = []
        self.validation_errors = []
        
    def append_message(self, message: str):
        self.logging_messages.append(message)
        self.external_messages.append(message)
        return self
    
    def append_to_log(self, message: str):
        self.logging_messages.append(message)
        return self

    def append_to_response(self, message: str):
        self.external_messages.append(message)
        return self
        
    def append_validation_error(self, message: str, subject: str = None):
        
        full_message = ""
        if subject is not None:
            full_message += subject + ": "
            
        full_message += message
        
        self.validation_errors.append(full_message)
        return self
        
    def has_validation_errors(self) -> bool:
        return len(self.validation_errors) > 0

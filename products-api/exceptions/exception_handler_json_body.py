from exceptions import http_status


class ExceptionHandlerJsonBody:
    
    def __init__(self,
                 status: http_status,
                 message: str,
                 error_code: str,
                 validation_errors: [],
                 data: []):
        self.status = status
        self.message = message
        self.error_code = error_code
        self.validation_errors = validation_errors
        self.data = data

    def get_json_format_dict(self) -> dict:
        return {
            "status": self.status.name,
            "error": self.message,
            "errorCode": self.error_code,
            "validation_errors": self.validation_errors,
            "messages": self.data
        }
    
from enum import Enum


class ExceptionType(Enum):
    BUSINESS_RULES = "BUSINESS_RULES"
    ERROR = "ERROR"
    VALIDATION = "VALIDATION"
    INTEGRATION = "INTEGRATION"

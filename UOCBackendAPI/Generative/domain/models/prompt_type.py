from enum import Enum

class PromptType(Enum):
    GENERATE_CONTENT = "GENERATE_CONTENT"
    GENERATE_SIMPLE = "GENERATE_SIMPLE"
    DETECT_LANGUAGE = "DETECT_LANGUAGE"
    REFORMULATE = "REFORMULATE"
    DESAMBIGUATION = "DESAMBIGUATION"
    CHECK_SUBJECT = "CHECK_SUBJECT"
    ADD_QUERY = "ADD_QUERY"
    HALLUTIONATION = "HALLUTIONATION"
    SUMARIZE = "SUMARIZE"
    APOLOGIZE = "APOLOGIZE"
    EVALUATION_MODEL_SYSTEM = "EVALUATION_MODEL_SYSTEM"
    EVALUATION_MODEL_USER = "EVALUATION_MODEL_USER"
    NOT_FOUND = ""

    @staticmethod
    def fromString(value: str):
        if value == "GENERATE_CONTENT":
            return PromptType.GENERATE_CONTENT
        if value == "GENERATE_SIMPLE":
            return PromptType.GENERATE_SIMPLE
        if value == "DETECT_LANGUAGE":
            return PromptType.DETECT_LANGUAGE
        if value == "REFORMULATE":
            return PromptType.REFORMULATE
        if value == "DESAMBIGUATION":
            return PromptType.DESAMBIGUATION
        if value == "CHECK_SUBJECT":
            return PromptType.CHECK_SUBJECT
        if value == "ADD_QUERY":
            return PromptType.ADD_QUERY
        if value == "HALLUTIONATION":
            return PromptType.HALLUTIONATION
        if value == "SUMARIZE":
            return PromptType.SUMARIZE
        if value == "APOLOGIZE":
            return PromptType.APOLOGIZE
        if value == "EVALUATION_MODEL_SYSTEM":
            return PromptType.EVALUATION_MODEL_SYSTEM
        if value == "EVALUATION_MODEL_USER":
            return PromptType.EVALUATION_MODEL_USER
        else:
            return PromptType.NOT_FOUND
    
    @staticmethod
    def getcode(type: Enum) -> str:
        if type == PromptType.GENERATE_CONTENT:
            return "1"
        if type == PromptType.GENERATE_SIMPLE:
            return "2"
        if type == PromptType.DETECT_LANGUAGE:
            return "3"
        if type == PromptType.REFORMULATE:
            return "4"
        if type == PromptType.DESAMBIGUATION:
            return "5"
        if type == PromptType.CHECK_SUBJECT:
            return "6"
        if type == PromptType.ADD_QUERY:
            return "7"
        if type == PromptType.HALLUTIONATION:
            return "8"
        if type == PromptType.SUMARIZE:
            return "9"
        if type == PromptType.APOLOGIZE:
            return "10"
        if type == PromptType.EVALUATION_MODEL_SYSTEM:
            return "11"
        if type == PromptType.EVALUATION_MODEL_USER:
            return "12"
        else:
            return "-1"

    def toString(self) -> str:
        return self.value
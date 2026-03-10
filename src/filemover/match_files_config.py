from enum import Enum
import os
import re

class FileMatchType(Enum):
    FILE_TYPE = "file_type"
    FILE_NAME = "file_name"

    @classmethod
    def from_string(cls, position: str) -> 'FileMatchType':
        if position.lower() not in cls._value2member_map_:
            raise ValueError(f"Invalid position: {position}. Must be one of {list(cls._value2member_map_.keys())}")
        return FileMatchType(cls._value2member_map_[position])
    
    @property
    def description(self) -> str:
        if self == FileMatchType.FILE_TYPE:
            return "Match file types"
        elif self == FileMatchType.FILE_NAME:
            return "Match file names"
        else:
            return "UNKNOWN"

class FileTypeMatchMode(Enum):
    SINGLE_EXACT = "single_exact"
    MULTIPLE_EXACT = "multiple_exact"
    REGEX_INCLUDE = "regex_include"
    REGEX_EXCLUDE = "regex_exclude"

    @classmethod
    def from_string(cls, position: str) -> 'FileTypeMatchMode':
        if position.lower() not in cls._value2member_map_:
            raise ValueError(f"Invalid position: {position}. Must be one of {list(cls._value2member_map_.keys())}")
        return FileTypeMatchMode(cls._value2member_map_[position])
    
    @property
    def description(self) -> str:
        if self == FileTypeMatchMode.SINGLE_EXACT:
            return "Match file types with a single extension"
        elif self == FileTypeMatchMode.MULTIPLE_EXACT:
            return "Match file types among a list of extensions"
        elif self == FileTypeMatchMode.REGEX_INCLUDE:
            return "Match file types using a regular expression"
        elif self == FileTypeMatchMode.REGEX_EXCLUDE:
            return "Match file types that aren't matched by a regular expression"
        else:
            return "UNKNOWN"

class FileNameMatchMode(Enum):
    SINGLE_EXACT = "single_exact"
    MULTIPLE_EXACT = "multiple_exact"
    CONTAINS = "contains"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"
    REGEX_INCLUDE = "regex_include"
    REGEX_EXCLUDE = "regex_exclude"

    @classmethod
    def from_string(cls, position: str) -> 'FileNameMatchMode':
        if position.lower() not in cls._value2member_map_:
            raise ValueError(f"Invalid position: {position}. Must be one of {list(cls._value2member_map_.keys())}")
        return FileNameMatchMode(cls._value2member_map_[position])
    
    @property
    def description(self) -> str:
        if self == FileNameMatchMode.SINGLE_EXACT:
            return "Match files with a single exact name"
        elif self == FileNameMatchMode.MULTIPLE_EXACT:
            return "Match files among a list of exact names"
        elif self == FileNameMatchMode.CONTAINS:
            return "Match files with a name containing a specific substring"
        elif self == FileNameMatchMode.STARTS_WITH:
            return "Match files with a name that starts with a specific substring"
        elif self == FileNameMatchMode.ENDS_WITH:
            return "Match files with a name that ends with a specific substring"
        elif self == FileNameMatchMode.REGEX_INCLUDE:
            return "Match files with a name that matches a regular expression"
        elif self == FileNameMatchMode.REGEX_EXCLUDE:
            return "Match files that have a name that doesn't match a regular expression"
        else:
            return "UNKNOWN"

class FileMatchRuleOperator(Enum):
    AND = "and"
    OR = "or"

    @classmethod
    def from_string(cls, position: str) -> 'FileMatchRuleOperator':
        if position.lower() not in cls._value2member_map_:
            raise ValueError(f"Invalid position: {position}. Must be one of {list(cls._value2member_map_.keys())}")
        return FileMatchRuleOperator(cls._value2member_map_[position])

    @property
    def description(self) -> str:
        if self == FileMatchRuleOperator.AND:
            return "AND (the conditions of all rules are satisfied)"
        elif self == FileMatchRuleOperator.OR:
            return "OR (the conditions of at least one of the rules are satisfied)"
        else:
            return "UNKNOWN"

class FileMatchRule:
    def __init__(self, **kwargs) -> None:
        type = kwargs.get("type")
        if not type:
            raise ValueError("Missing parameter ""type"" from File Match rule")
        if type not in FileMatchType:
            raise ValueError(f'Parameter "type" must be one of the following values: {', '.join([member.value for member in FileMatchType])}')
        self.type = FileMatchType.from_string(type)
        
        mode = kwargs.get("mode")
        if not mode:
            raise ValueError("Missing parameter ""mode"" from File Match rule")

        if self.type == FileMatchType.FILE_TYPE:
            self.mode = FileTypeMatchMode.from_string(mode)
        elif self.type == FileMatchType.FILE_NAME:
            self.mode = FileNameMatchMode.from_string(mode)
            self.case_sensitive = kwargs.get("case_sensitive", True)
        else:
            raise ValueError("Invalid File Match Rule type")

        value = kwargs.get("value")
        if not value:
            raise ValueError("Missing parameter ""value"" from File Match rule")
        self.value = value
        
    
    def matches_file(self, file_path: str) -> bool:
        name, extension = os.path.splitext(file_path)
        extension = extension[1:]

        if self.type == FileMatchType.FILE_TYPE:
            if self.mode == FileTypeMatchMode.SINGLE_EXACT:
                if not isinstance(self.value, str):
                    raise ValueError(f'Invalid File Match Rule type. "{self.mode.value}" rule "value" must be a string for "{self.type.value}"')
                return extension == self.value
            elif self.mode == FileTypeMatchMode.MULTIPLE_EXACT:
                if not isinstance(self.value, list):
                    raise ValueError(f'Invalid File Match Rule type. "{self.mode.value}" rule "value" must be a list for "{self.type.value}"')
                return extension in self.value
            elif self.mode == FileTypeMatchMode.REGEX_INCLUDE:
                if not isinstance(self.value, str):
                    raise ValueError(f'Invalid File Match Rule type. "{self.mode.value}" rule "value" must be a string for "{self.type.value}"')
                return re.match(self.value, extension) is not None
            elif self.mode == FileTypeMatchMode.REGEX_EXCLUDE:
                if not isinstance(self.value, str):
                    raise ValueError(f'Invalid File Match Rule type. "{self.mode.value}" rule "value" must be a string for "{self.type.value}"')
                return re.match(self.value, extension) is None
        elif self.type == FileMatchType.FILE_NAME:
            if self.mode == FileNameMatchMode.SINGLE_EXACT:
                if self.case_sensitive:
                    return name.lower() == self.value.lower()
                return name == self.value
            elif self.mode == FileNameMatchMode.MULTIPLE_EXACT:
                if self.case_sensitive:
                    return name.lower() in [v.lower() for v in self.value]
                return name in self.value
            elif self.mode == FileNameMatchMode.CONTAINS:
                if self.case_sensitive:
                    return self.value.lower() in name.lower()
                return self.value in name
            elif self.mode == FileNameMatchMode.STARTS_WITH:
                if self.case_sensitive:
                    return name.lower().startswith(self.value.lower())
                return name.startswith(self.value)
            elif self.mode == FileNameMatchMode.ENDS_WITH:
                if self.case_sensitive:
                    return name.lower().endswith(self.value.lower())
                return name.endswith(self.value)
            elif self.mode == FileNameMatchMode.REGEX_INCLUDE:
                return re.match(self.value, name) is not None
            elif self.mode == FileNameMatchMode.REGEX_EXCLUDE:
                return re.match(self.value, name) is None
        else:
            raise ValueError("Invalid File Match Rule type")
        
        raise ValueError("Invalid File Match Rule configuration")

class FileMatchConfig:
    def __init__(self, **kwargs) -> None:
        self.enabled = kwargs.get("enabled", True)
        self.operator = FileMatchRuleOperator.from_string(kwargs.get("operator", "and"))
        self.rules = [FileMatchRule(**rule) for rule in kwargs.get('rules', [])]
    
    def matches_file(self, file_path: str) -> bool:
        if not self.enabled:
            return True
        
        if self.operator == FileMatchRuleOperator.AND:
            return all(rule.matches_file(file_path) for rule in self.rules)
        elif self.operator == FileMatchRuleOperator.OR:
            return any(rule.matches_file(file_path) for rule in self.rules)
        
        raise ValueError("Invalid File Match configuration")

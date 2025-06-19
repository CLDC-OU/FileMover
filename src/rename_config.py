import pytz
from datetime import datetime
from enum import Enum

class RenameRule:
    def __init__(self, search: str, replace: str):
        self.search = search
        self.replace = replace

    def __repr__(self):
        return f"RenameRule(search='{self.search}', replace='{self.replace}')"

class TimestampPosition(Enum):
    START = 'start'
    AFTER_PREFIX = 'after_prefix'
    BEFORE_SUFFIX = 'before_suffix'
    END = 'end'

    @classmethod
    def from_string(cls, position: str) -> 'TimestampPosition':
        if position not in cls._value2member_map_:
            raise ValueError(f"Invalid position: {position}. Must be one of {list(cls._value2member_map_.keys())}.")
        return TimestampPosition(cls._value2member_map_[position])

class AddTimestampConfig:
    def __init__(self, **kwargs):
        self._enabled = kwargs.get('enabled', False)
        self._format = kwargs.get('format', '%Y-%m-%d_%H-%M-%S')
        self._timezone = kwargs.get('timezone', 'UTC')
        self._position = TimestampPosition.from_string(kwargs.get('position', 'after_prefix'))

        if not isinstance(self._enabled, bool):
            raise TypeError("Enabled must be a boolean value")
        self._enabled = self._enabled

        if not self._timezone or not isinstance(self._timezone, str):
            # Set default to local timezone if not provided
            self._timezone = datetime.now().astimezone().tzinfo
        elif self._timezone in pytz.all_timezones:
            self._timezone = pytz.timezone(self._timezone)
        else:
            raise ValueError(f"Invalid timezone: {self._timezone}. Must be a valid timezone string.")

        if self._position not in [TimestampPosition.START, TimestampPosition.AFTER_PREFIX, TimestampPosition.BEFORE_SUFFIX, TimestampPosition.END]:
            raise ValueError(f"Invalid position: {self._position}. Must be one of {TimestampPosition.START}, {TimestampPosition.AFTER_PREFIX}, {TimestampPosition.BEFORE_SUFFIX}, {TimestampPosition.END}.")
        if not isinstance(self._format, str):
            raise TypeError("Format must be a string")

    @property
    def enabled(self) -> bool:
        return self._enabled
    
    @property
    def position(self) -> 'TimestampPosition':
        return self._position

    def get_timestamp(self):
        return datetime.now(self._timezone).strftime(self._format)

class RenameConfig:
    def __init__(self, **kwargs):
        self._enabled = kwargs.get('enabled', False)
        self._replace_rules = [RenameRule(**rule) for rule in kwargs.get('replace', [])]
        self._case_sensitive = kwargs.get('case_sensitive', False)
        self._prefix = kwargs.get('prefix', '')
        self._suffix = kwargs.get('suffix', '')
        self._add_timestamp = AddTimestampConfig(**kwargs.get('add_timestamp', {}))

    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    def replace_rules(self) -> list[RenameRule]:
        return self._replace_rules

    @property
    def case_sensitive(self) -> bool:
        return self._case_sensitive

    @property
    def prefix(self) -> str:
        return self._prefix

    @property
    def suffix(self) -> str:
        return self._suffix

    @property
    def add_timestamp(self) -> AddTimestampConfig:
        return self._add_timestamp
    
    def apply_rename(self, file_name: str) -> str:
        if not self.enabled:
            return file_name
        if not file_name:
            raise ValueError("File name cannot be empty")

        # Apply replace rules
        for rule in self.replace_rules:
            if self.case_sensitive:
                file_name = file_name.replace(rule.search, rule.replace)
            else:
                file_name = file_name.lower().replace(rule.search.lower(), rule.replace)

        # Add the timestamp if relative to prefix or suffix
        if self.add_timestamp.enabled and self.add_timestamp.position == TimestampPosition.AFTER_PREFIX:
            file_name = f"{self.add_timestamp.get_timestamp()}_{file_name}"
        elif self.add_timestamp.enabled and self.add_timestamp.position == TimestampPosition.BEFORE_SUFFIX:
            file_name = f"{file_name}_{self.add_timestamp.get_timestamp()}"

        # Add prefix and suffix
        if self.prefix:
            file_name = f"{self.prefix}{file_name}"
        if self.suffix:
            file_name = f"{file_name}{self.suffix}"

        # Add timestamp at the start or end
        if self.add_timestamp.enabled:
            if self.add_timestamp.position == TimestampPosition.START:
                file_name = f"{self.add_timestamp.get_timestamp()}_{file_name}"
            elif self.add_timestamp.position == TimestampPosition.END:
                file_name = f"{file_name}_{self.add_timestamp.get_timestamp()}"

        # Ensure the file name is not empty after renaming
        if not file_name:
            raise ValueError("The resulting file name cannot be empty after applying rename rules.")

        return file_name
from __future__ import annotations
from .rename_config import RenameConfig
from .match_files_config import FileMatchConfig
from enum import Enum

class KeepSourceBehavior(Enum):
    NEVER_KEEP_SOURCE = 'never_keep_source'
    ALWAYS_KEEP_SOURCE = 'keep_source'
    KEEP_SOURCE_IF_ANY_COLLIDE = 'keep_source_if_any_collide'
    KEEP_SOURCE_IF_ALL_COLLIDE = 'keep_source_if_all_collide'
    KEEP_SOURCE_IF_NONE_COLLIDE = 'keep_source_if_none_collide'

    @classmethod
    def from_string(cls, position: str) -> 'KeepSourceBehavior':
        if position not in cls._value2member_map_:
            raise ValueError(f"Invalid position: {position}. Must be one of {list(cls._value2member_map_.keys())}")
        return KeepSourceBehavior(cls._value2member_map_[position])
    
    @property
    def description(self) -> str:
        if self == KeepSourceBehavior.NEVER_KEEP_SOURCE:
            return "Delete the source file (i.e., 'move' the file)"
        elif self == KeepSourceBehavior.ALWAYS_KEEP_SOURCE:
            return "Keep the source file (i.e., 'copy' the file)"
        elif self == KeepSourceBehavior.KEEP_SOURCE_IF_ANY_COLLIDE:
            return "Keep the source file if ANY destination files collide (delete otherwise)"
        elif self == KeepSourceBehavior.KEEP_SOURCE_IF_ALL_COLLIDE:
            return "Keep the source file if ALL destination files collide (delete otherwise)"
        elif self == KeepSourceBehavior.KEEP_SOURCE_IF_NONE_COLLIDE:
            return "Keep the source file if NO destination files collide (i.e., delete if any collide)"
        else:
            return "UNKNOWN"

class CollisionAvoidanceBehavior(Enum):
    NONE = 'none'
    CANCEL_MOVE_IF_ANY_COLLIDE = 'cancel_move_if_any_collide'
    CANCEL_MOVE_IF_ALL_COLLIDE = 'cancel_move_if_all_collide'

    @classmethod
    def from_string(cls, position: str) -> 'CollisionAvoidanceBehavior':
        if position not in cls._value2member_map_:
            raise ValueError(f"Invalid position: {position}. Must be one of {list(cls._value2member_map_.keys())}")
        return CollisionAvoidanceBehavior(cls._value2member_map_[position])
    
    @property
    def description(self) -> str:
        if self == CollisionAvoidanceBehavior.NONE:
            return "Continue with the move operation"
        elif self == CollisionAvoidanceBehavior.CANCEL_MOVE_IF_ANY_COLLIDE:
            return "Cancel the move operation if any files would collide"
        elif self == CollisionAvoidanceBehavior.CANCEL_MOVE_IF_ALL_COLLIDE:
            return "Cancel the move operation if all files would collide"
        else:
            return "UNKNOWN"

class DestinationCollisionBehavior(Enum):
    IGNORE = 'ignore'
    OVERWRITE = 'overwrite'

    @classmethod
    def from_string(cls, position: str) -> 'DestinationCollisionBehavior':
        if position not in cls._value2member_map_:
            raise ValueError(f"Invalid position: {position}. Must be one of {list(cls._value2member_map_.keys())}")
        return DestinationCollisionBehavior(cls._value2member_map_[position])

    @property
    def description(self) -> str:
        if self == DestinationCollisionBehavior.IGNORE:
            return "Ignore/skip the file move operation (do nothing) and proceed"
        elif self == DestinationCollisionBehavior.OVERWRITE:
            return "Overwrite the existing file"
        else:
            return "UNKNOWN"

class MoverConfig:
    def __init__(self, **kwargs):
        self._mover_name = kwargs.get('mover_name', 'default_mover')
        self._mover_description = kwargs.get('mover_description', 'No description provided')

        if 'source_directory' in kwargs:
            self._source_directories = [kwargs['source_directory']]
        else:
            self._source_directories = kwargs.get('source_directories', [])

        self._match_files_config =  FileMatchConfig(**kwargs.get('match_files', {}))

        if 'destination_directory' in kwargs:
            self._destination_directories = [kwargs['destination_directory']]
        else:
            self._destination_directories = kwargs.get('destination_directories', [])

        self._rename_config = RenameConfig(**kwargs.get('rename', {}))
        if not self._rename_config.enabled:
            self._rename_config = None

        self._keep_source_behavior = KeepSourceBehavior.from_string(kwargs.get('keep_source_behavior', 'never_keep_source'))
        self._recursive = kwargs.get('recursive', False)
        self._destination_collision_behavior = DestinationCollisionBehavior.from_string(kwargs.get('destination_collision_behavior', 'ignore'))
        self._collision_avoidance_behavior = CollisionAvoidanceBehavior.from_string(kwargs.get('collision_avoidance_behavior', 'none'))
        self._validate()

    def __str__(self):
        return self._mover_name
    def __repr__(self):
        return f"MoverConfig(name={self._mover_name}, description={self._mover_description})"

    @property
    def mover_name(self) -> str:
        return self._mover_name
    @property
    def mover_description(self) -> str:
        return self._mover_description
    @property
    def source_directories(self) -> list:
        return self._source_directories
    @property
    def destination_directories(self) -> list:
        return self._destination_directories
    @property
    def match_files_config(self) -> FileMatchConfig:
        return self._match_files_config
    @property
    def rename_config(self) -> RenameConfig | None:
        return self._rename_config
    @property
    def keep_source_behavior(self) -> KeepSourceBehavior:
        return self._keep_source_behavior
    @property
    def recursive(self) -> bool:
        return self._recursive
    @property
    def destination_collision_behavior(self) -> 'DestinationCollisionBehavior':
        return self._destination_collision_behavior
    @property
    def collision_avoidance_behavior(self) -> 'CollisionAvoidanceBehavior':
        return self._collision_avoidance_behavior

    def _validate(self):
        if not self._source_directories or len(self._source_directories) < 1:
            raise ValueError("At least one source directory must be specified")
        if not self._destination_directories or len(self._destination_directories) < 1:
            raise ValueError("At least one destination directory must be specified")
        
        # TODO: Add validation functions to sub-configs and check them here
        if self._match_files_config and not isinstance(self._match_files_config, FileMatchConfig):
            raise ValueError('Property "match_files" must be an instance of FileMatchConfig')
        if self._rename_config and not isinstance(self._rename_config, RenameConfig):
            raise ValueError('Property "rename" must be an instance of RenameConfig')
        if self._match_files_config and not isinstance(self._match_files_config, FileMatchConfig):
            raise ValueError('Property "match_files" must be an instance of FileMatchConfig')

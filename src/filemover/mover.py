from __future__ import annotations
from .mover_config import MoverConfig, DestinationCollisionBehavior, KeepSourceBehavior, CollisionAvoidanceBehavior
from .logger import logger
import shutil
import os
import re

class Mover:
    def __init__(self, **kwargs):
        self.config = MoverConfig(**kwargs)

    def __str__(self):
        return f"{self.config.mover_name}: {self.config.mover_description}"

    def __repr__(self):
        return f"Mover(name={self.config.mover_name}, description={self.config.mover_description})"

    def _should_move_file(self, file_name):
        if not file_name:
            return False
        
        file_type = os.path.splitext(file_name)[1][1:]  # Get file extension without dot
        file_name = os.path.splitext(file_name)[0]

        # Verify file type
        if self.config.file_types and not any(file_type == ext for ext in self.config.file_types):
            return False
        if self.config.file_type_regex and not re.match(self.config.file_type_regex, file_type):
            return False
        if self.config.file_type_exclude_regex and re.match(self.config.file_type_exclude_regex, file_type):
            return False

        # Verify file name
        if self.config.file_names and file_name not in self.config.file_names:
            return False
        if self.config.file_name_regex and not re.match(self.config.file_name_regex, file_name):
            return False
        if self.config.file_name_exclude_regex and re.match(self.config.file_name_exclude_regex, file_name):
            return False
        if self.config.file_name_contains and self.config.file_name_contains not in file_name:
            return False
        if self.config.file_name_starts_with and not file_name.startswith(self.config.file_name_starts_with):
            return False
        if self.config.file_name_ends_with and not file_name.endswith(self.config.file_name_ends_with):
            return False
        
        return True

    def _copy_file(self, source_file_path, destination_file_path):
        destination_directory = os.path.dirname(destination_file_path)
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)
        
        logger.info(f"Copying file \"{source_file_path}\" to \"{destination_file_path}\"")

        if os.path.exists(destination_file_path):
            if self.config.keep_source_behavior == DestinationCollisionBehavior.IGNORE:
                logger.info(f"\tFile \"{destination_file_path}\" already exists. Skipping copy")
                return
        shutil.copy2(source_file_path, destination_file_path)
        logger.info(f"\tSuccessfully copied file \"{source_file_path}\" to \"{destination_file_path}\"")

    def _handle_source_file_removal(self, source_path, destinations, collisions):
        if self.config.keep_source_behavior == KeepSourceBehavior.ALWAYS_KEEP_SOURCE:
            should_remove = False
        elif self.config.keep_source_behavior == KeepSourceBehavior.KEEP_SOURCE_IF_ANY_COLLIDE:
            should_remove = len(collisions) > 0
        elif self.config.keep_source_behavior == KeepSourceBehavior.KEEP_SOURCE_IF_ALL_COLLIDE:
            should_remove = len(collisions) > len(destinations)
        elif self.config.keep_source_behavior == KeepSourceBehavior.KEEP_SOURCE_IF_NONE_COLLIDE:
            should_remove = len(collisions) == 0
        elif self.config.keep_source_behavior == KeepSourceBehavior.NEVER_KEEP_SOURCE:
            should_remove = True
        else:
            should_remove = False

        if should_remove:
            os.remove(source_path)
            logger.info(f"Removed source file \"{source_path}\"")

    def _get_destination_files_for_source(self, source_path) -> tuple[list, list]:
        collisions = []
        destinations = []
        
        # Collision checking
        for destination_directory in self.config.destination_directories:
            destination_file_path = self.get_destination_file_path(source_path, destination_directory)
            destinations.append(destination_file_path)
            if os.path.exists(destination_file_path):
                collisions.append(destination_file_path)
        
        return destinations, collisions

    def _should_skip_move(self, destinations, collisions) -> bool:
        if self.config.collision_avoidance_behavior == CollisionAvoidanceBehavior.CANCEL_MOVE_IF_ANY_COLLIDE:
            if len(collisions) > 0:
                return True
        elif self.config.collision_avoidance_behavior == CollisionAvoidanceBehavior.CANCEL_MOVE_IF_ALL_COLLIDE:
            if len(collisions) == len(destinations):
                return True
        return False

    def get_matched_files(self) -> list[str]:
        """
        Returns a list of paths of all files that match the mover's criteria
        """
        matched_files = []
        if not self.config.source_directories:
            raise ValueError("Source directories must be specified.")
        for source_dir in self.config.source_directories:
            if self.config.recursive:
                walker = os.walk(source_dir)
            else:
                walker = [(source_dir, [], os.listdir(source_dir))]
            for root, _, files in walker:
                for file_name in files:
                    if self._should_move_file(file_name):
                        matched_files.append(os.path.join(root, file_name))
        return matched_files

    def list_matched_files(self) -> None:
        logger.info(f"Matched files for \"{self.config}\":")
        for matched_file in self.get_matched_files():
            logger.info(f"\t\"{matched_file}\"")

    def matches_filename(self, file_name) -> bool:
        """
        Check if the given file matches the mover's criteria
        """
        return self._should_move_file(file_name)

    def get_mover_config(self) -> MoverConfig:
        """
        Get the mover's configuration
        """
        return self.config

    def set_mover_config(self, config: MoverConfig):
        """
        Set the mover's configuration
        """
        config._validate()
        self.config = config

    def get_destination_file_path(self, source_path, destination_directory):
        if self.config.rename_config:
            logger.info(f"\tApplying rename configuration: {self.config.rename_config}")
            destination_file_name = self.config.rename_config.apply_rename(os.path.basename(source_path)) if self.config.rename_config else os.path.basename(source_path)
            logger.info(f"\tRenaming file to \"{destination_file_name}\"")
        else:
            destination_file_name = os.path.basename(source_path)
        return os.path.join(destination_directory, destination_file_name)

    def move_files(self):
        """
        Runs the mover based on its configuration to move (or copy) all files in the source directories to the configured destination directories
        """
        logger.info(f"Starting mover \"{self.config}\"")
        if not self.config.source_directories or not self.config.destination_directories:
            raise ValueError("Source and destination directories must be specified.")
        for source_dir in self.config.source_directories:
            if self.config.recursive:
                walker = os.walk(source_dir)
            else:
                walker = [(source_dir, [], os.listdir(source_dir))]

            for root, _, files in walker:
                for file_name in files:
                    if not self._should_move_file(file_name):
                        continue

                    source_path = os.path.join(root, file_name)
                    destinations, collisions = self._get_destination_files_for_source(source_path)
                    logger.info(f"File \"{file_name}\" matched on mover \"{self.config}\" with {len(destinations)} destination(s) and {len(collisions)} collision(s)")

                    if self._should_skip_move(destinations, collisions):
                        logger.info(f"{len(collisions)} collision(s) would result from the current move operation - this file will be skipped: \"{source_path}\"")
                        continue

                    # File Copying
                    for destination_file_path in destinations:
                        self._copy_file(source_path, destination_file_path)

                    # Source File Removal
                    self._handle_source_file_removal(source_path, destinations, collisions)

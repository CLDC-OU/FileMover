from __future__ import annotations
from filemover.mover_config import MoverConfig, DestinationCollisionBehavior, KeepSourceBehavior, CollisionAvoidanceBehavior
from filemover.logger import create_logger
from filemover.metadata import Metadata, ExecutionResults
import shutil
import os

class Mover:
    def __init__(self, **kwargs):
        log_file = kwargs.get('log_file', None)
        verbose = kwargs.get('verbose', True)
        self.mover_id = kwargs.get('id', None)
        metadata_file = kwargs.get('metadata_file', 'filemover.json')
        self.config = MoverConfig(**kwargs)
        self.logger = create_logger(self.config.mover_name, verbose, log_file)
        if self.mover_id:
            self.metadata = Metadata(metadata_file)

    def __str__(self):
        return f"{self.config.mover_name}: {self.config.mover_description}"

    def __repr__(self):
        return f"Mover(name={self.config.mover_name}, description={self.config.mover_description})"

    def _copy_file(self, source_file_path, destination_file_path) -> bool:
        destination_directory = os.path.dirname(destination_file_path)
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)
        
        self.logger.debug(f"Copying file \"{source_file_path}\" to \"{destination_file_path}\"")

        if os.path.exists(destination_file_path):
            if self.config.keep_source_behavior == DestinationCollisionBehavior.IGNORE:
                self.logger.warning(f"File \"{destination_file_path}\" already exists. Skipping copy")
                return False
        shutil.copy2(source_file_path, destination_file_path)
        self.logger.debug(f"Successfully copied file \"{source_file_path}\" to \"{destination_file_path}\"")
        return True

    def _handle_source_file_removal(self, source_path, destinations, collisions) -> bool:
        if self.config.keep_source_behavior == KeepSourceBehavior.ALWAYS_KEEP_SOURCE:
            should_remove = False
        elif self.config.keep_source_behavior == KeepSourceBehavior.KEEP_SOURCE_IF_ANY_COLLIDE:
            should_remove = len(collisions) == 0
        elif self.config.keep_source_behavior == KeepSourceBehavior.KEEP_SOURCE_IF_ALL_COLLIDE:
            should_remove = len(collisions) < len(destinations)
        elif self.config.keep_source_behavior == KeepSourceBehavior.KEEP_SOURCE_IF_NONE_COLLIDE:
            should_remove = len(collisions) > 0
        elif self.config.keep_source_behavior == KeepSourceBehavior.NEVER_KEEP_SOURCE:
            should_remove = True
        else:
            should_remove = False

        if should_remove:
            os.remove(source_path)
            self.logger.debug(f"Removed source file \"{source_path}\"")
            return True
        return False

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
        Return a list of paths of all files that match the mover's criteria
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
                    if self.matches_filename(file_name):
                        matched_files.append(os.path.join(root, file_name))
        return matched_files

    def list_matched_files(self) -> None:
        """
        Log the path for each file that matches the mover's criteria
        """
        self.logger.info(f"Matched files for \"{self.config}\":")
        for matched_file in self.get_matched_files():
            self.logger.info(f"\t\"{matched_file}\"")
    
    def matches_filename(self, file_name) -> bool:
        """
        Return True if the provided filename matches the mover's criteria\n
        ---\n
        Keyword arguments:\n
        file_name -- the name of the file to check
        """
        if not file_name:
            return False
        return self.config.match_files_config.matches_filename(file_name)

    def get_mover_config(self) -> MoverConfig:
        """
        Get the mover's configuration
        """
        return self.config

    def set_mover_config(self, config: MoverConfig):
        """
        Set the mover's configuration\n
        ---\n
        Keyword arguments:\n
        config -- the MoverConfig to use for the mover 
        """
        config._validate()
        self.config = config

    def get_destination_file_path(self, source_path, destination_directory):
        """
        Get the destination path for a source file, with any configuration rules applied (e.g., renaming)\n
        ---\n
        Keyword arguments:\n
        source_path -- a full path to a file to consider as the source\n
        destination_directory -- the directory that the returned destination file path should have
        """
        if self.config.rename_config:
            self.logger.debug(f"Applying rename configuration: {self.config.rename_config}")
            destination_file_name = self.config.rename_config.apply_rename(os.path.basename(source_path)) if self.config.rename_config else os.path.basename(source_path)
            self.logger.debug(f"Renaming file to \"{destination_file_name}\"")
        else:
            destination_file_name = os.path.basename(source_path)
        return os.path.join(destination_directory, destination_file_name)

    def _run_move_files(self) -> ExecutionResults:
        results = ExecutionResults()
        try:
            if not self.config.source_directories or not self.config.destination_directories:
                raise ValueError("Source and destination directories must be specified.")
            for source_dir in self.config.source_directories:
                if self.config.recursive:
                    walker = os.walk(source_dir)
                else:
                    walker = [(source_dir, [], os.listdir(source_dir))]

                for root, _, files in walker:
                    for file_name in files:
                        is_copied = False
                        is_deleted = False

                        if not self.matches_filename(file_name):
                            continue

                        source_path = os.path.join(root, file_name)
                        destinations, collisions = self._get_destination_files_for_source(source_path)
                        self.logger.debug(f"File \"{file_name}\" matched on mover \"{self.config}\" with {len(destinations)} destination(s) and {len(collisions)} collision(s)")

                        if self._should_skip_move(destinations, collisions):
                            self.logger.debug(f"{len(collisions)} collision(s) would result from the current move operation - this file will be skipped: \"{source_path}\"")
                            continue

                        # File Copying
                        copied_count = 0
                        skipped_count = 0
                        for destination_file_path in destinations:
                            is_copied = self._copy_file(source_path, destination_file_path)
                            if is_copied:
                                copied_count += 1
                            else:
                                skipped_count += 1

                        # Source File Removal
                        is_deleted = self._handle_source_file_removal(source_path, destinations, collisions)
                        
                        if copied_count > 0 and is_deleted:
                            results.increment_moved(copied_count)
                        elif copied_count > 0:
                            results.increment_copied(copied_count)
                        elif is_deleted:
                            results.increment_deleted()
                        
                        results.increment_skipped(skipped_count)

        except BaseException as e:
            results.increment_errors()
        
        return results

    def move_files(self):
        """
        Run the mover based on its configuration to move (or copy) all files in the source directories to the configured destination directories
        """
        self.logger.debug(f"Starting mover \"{self.config}\"")
        results = self._run_move_files()
        messages = []
        if results.moved > 0:
            messages.append(f"Moved {results.moved} file{'' if results.moved == 1 else 's'}")
        if results.copied > 0:
            messages.append(f"Copied {results.copied} file{'' if results.copied == 1 else 's'}")
        if results.deleted > 0:
            messages.append(f"Deleted {results.deleted} file{'' if results.deleted == 1 else 's'}")
        message = f"Mover \"{self.config.mover_name}\" completed"
        if len(messages) > 0:
            message = message + "\n\t" + '\n\t'.join(messages)
        else:
            message = message + " - no files to move"
        self.logger.info(message)
        if self.mover_id:
            self.metadata.update(self.mover_id, results)

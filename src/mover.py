from src.mover_config import MoverConfig
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

    def _copy_file(self, source_path, destination_path):
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        
        print(f"Copying file {source_path} to {destination_path}")
        if self.config.rename_config:
            print(f"\tApplying rename configuration: {self.config.rename_config}")
            destination_file_name = self.config.rename_config.apply_rename(os.path.basename(source_path)) if self.config.rename_config else os.path.basename(source_path)
            print(f"\tRenaming file to {destination_file_name}")
        else:
            destination_file_name = os.path.basename(source_path)
        destination_file_path = os.path.join(destination_path, destination_file_name)
        if os.path.exists(destination_file_path):
            print(f"\tFile {destination_file_path} already exists. Skipping copy.")
            return
        shutil.copy2(source_path, destination_file_path)
        print(f"\tSuccessfully copied file {source_path} to {destination_file_path}")

    def move_files(self):
        print(f"Starting mover {self.config}")
        if not self.config.source_directories or not self.config.destination_directories:
            raise ValueError("Source and destination directories must be specified.")
        for source_dir in self.config.source_directories:
            for root, _, files in os.walk(source_dir):
                for file_name in files:
                    if self._should_move_file(file_name):
                        print(f"File {file_name} matched on mover {self.config}")
                        source_path = os.path.join(root, file_name)
                        for dest_dir in self.config.destination_directories:
                            self._copy_file(source_path, dest_dir)
                        if not self.config.keep_source:
                            os.remove(source_path)
                            print(f"Removed source file {source_path}")

from src.filemover.rename_config import TimestampPosition

from colorama import Fore, Style
import os
import pytz
import json

SET_INFO_COLOR = Fore.LIGHTBLACK_EX
SET_PARAMETER_COLOR = Fore.LIGHTCYAN_EX
SET_VALUE_COLOR = Fore.LIGHTYELLOW_EX
PARAMETER_COLOR = Fore.CYAN
VALUE_COLOR = Fore.YELLOW
MENU_OPTION_VALUE_COLOR = Fore.MAGENTA
MENU_OPTION_NAME_COLOR = Fore.BLUE
WARNING_COLOR = Fore.LIGHTRED_EX
ERROR_COLOR = Fore.RED

class MoverConfigBuilder:
    def __init__(self):
        self.multiple_sources = False
        self.multiple_destinations = False
        self.config = {}

#=====Validator Helpers=====================================
    def _validate_path(self, path):
        if not path or not path.strip():
            raise ValueError(f"{ERROR_COLOR}Path cannot be empty{Style.RESET_ALL}")
        if not isinstance(path, str):
            raise ValueError(f"{ERROR_COLOR}Path must be a string{Style.RESET_ALL}")
        if not os.path.isabs(path):
            raise ValueError(f"{ERROR_COLOR}Path must be an absolute path{Style.RESET_ALL}")

    def _is_valid_path(self, path):
        if not path or not path.strip():
            return False
        if not isinstance(path, str):
            return False
        if not os.path.isabs(path):
            return False
        return True

    def _is_valid_regex(self, pattern):
        import re
        try:
            re.compile(pattern)
            return True
        except re.error:
            return False
#===========================================================

#=====Config Value Helpers==================================
    def _try_set_option(self, option, value):
        try:
            if option == 'source_directory':
                self.set_source_directory(value)
            elif option == 'source_directories':
                self.set_source_directories(value)
            elif option == 'destination_directory':
                self.set_destination_directory(value)
            elif option == 'destination_directories':
                self.set_destination_directories(value)
            elif option == 'file_type':
                self.set_file_type(value)
            elif option == 'file_types':
                self.set_file_types(value)
            elif option == 'file_type_regex':
                self.set_file_type_regex(value)
            elif option == 'file_type_exclude_regex':
                self.set_file_type_exclude_regex(value)
            elif option == 'file_name':
                self.set_file_name(value)
            elif option == 'file_names':
                self.set_file_names(value)
            elif option == 'file_name_contains':
                self.set_file_name_contains(value)
            elif option == 'file_name_starts_with':
                self.set_file_name_starts_with(value)
            elif option == 'file_name_ends_with':
                self.set_file_name_ends_with(value)
            elif option == 'file_name_regex':
                self.set_file_name_regex(value)
            elif option == 'file_name_exclude_regex':
                self.set_file_name_exclude_regex(value)
            elif option == 'recursive':
                self.set_recursive(value)
            elif option == 'keep_source':
                self.set_keep_source(value)
            elif option == 'name':
                self.set_name(value)
            elif option == 'description':
                self.set_description(value)
            else:
                raise ValueError(f"{ERROR_COLOR}Unknown config option '{option}'")
        except ValueError as e:
            print(e)
            return False
        return True

    def _try_set_rename_option(self, option, value):
        try:
            if option == 'case_sensitive':
                self.set_rename_case_sensitive(value)
            elif option == 'prefix':
                self.set_rename_prefix(value)
            elif option == 'suffix':
                self.set_rename_suffix(value)
            else:
                raise ValueError(f"{ERROR_COLOR}Unknown rename config option '{option}'")
        except ValueError as e:
            print(e)
            return False
        return True

    def _try_set_timestamp_option(self, option, value):
        try:
            if option == 'format':
                self.set_rename_timestamp_format(value)
            elif option == 'timezone':
                self.set_rename_timestamp_timezone(value)
            elif option == 'position':
                self.set_rename_timestamp_position(value)
            else:
                raise ValueError(f"{ERROR_COLOR}Unknown rename timestamp config option '{option}'")
        except ValueError as e:
            print(e)
            return False
        return True

    def _create_or_get_rename(self):
        rename = self.config.get("rename")
        if not rename:
            rename = {}
            rename["enabled"] = True
        return rename
    def _create_or_get_timestamp(self):
        rename = self._create_or_get_rename()
        timestamp = rename.get("timestamp")
        if not timestamp:
            timestamp = {}
            timestamp["enabled"] = True
        return timestamp
#===========================================================

    def _print_set_message(self, option, value, value_detail = None):
        print(f"{SET_INFO_COLOR}Set {f'{value_detail} ' if value_detail else ''}{SET_PARAMETER_COLOR}{option}{Style.RESET_ALL}{SET_INFO_COLOR} to {SET_VALUE_COLOR}{value}{Style.RESET_ALL}\n")

#=====Config Value Setters==================================
    def set_rename_case_sensitive(self, value):
        if not isinstance(value, bool):
            raise ValueError(f"{ERROR_COLOR}Case Sensitive must be a boolean value{Style.RESET_ALL}")
        rename = self._create_or_get_rename()
        rename['case_sensitive'] = value
        self.config['rename'] = rename
        self._print_set_message("Case Sensitive", value, 'rename')
        return self
    def set_rename_prefix(self, value):
        if not value or len(value) < 1:
            return
        rename = self._create_or_get_rename()
        rename['prefix'] = value
        self.config['rename'] = rename
        self._print_set_message("Prefix", value, 'rename')
        return self
    def set_rename_suffix(self, value):
        if not value or len(value) < 1:
            return
        rename = self._create_or_get_rename()
        rename['suffix'] = value
        self.config['rename'] = rename
        self._print_set_message("Suffix", value, 'rename')
        return self
    def add_replace_rule(self, value):
        if not 'search' in value or len(value['search']) < 1:
            raise ValueError(f"{ERROR_COLOR}Search must not be blank in replace rule{Style.RESET_ALL}")
        if not 'replace' in value:
            value['replace'] = ""
        
        rename = self._create_or_get_rename()
        if 'replace' not in rename:
            rename['replace'] = []
        rename['replace'].append(value)
        self.config['rename'] = rename
        print(f"{SET_INFO_COLOR}Added rename Replace Rule: {SET_PARAMETER_COLOR}Search{Style.RESET_ALL}{SET_INFO_COLOR}: {SET_VALUE_COLOR}{value['search']}{Style.RESET_ALL}{SET_INFO_COLOR}, Replace: {SET_VALUE_COLOR}{value['replace'] if len(value['replace']) > 0 else f'{ERROR_COLOR}<REMOVE>{Style.RESET_ALL}'}{Style.RESET_ALL}")
        return self
    
    def set_rename_timestamp_format(self, value):
        timestamp = self._create_or_get_timestamp()
        if not value or len(value) < 1:
            timestamp["format"] = None
            return
        # TODO: Add timestamp format verification
        timestamp["format"] = value
        self.config['rename']['timestamp'] = timestamp
        self._print_set_message("Timestamp Format", value, 'rename')
        return self
    def set_rename_timestamp_timezone(self, value):
        timestamp = self._create_or_get_timestamp()
        if not value or len(value) < 1:
            timestamp["timezone"] = None
            return
        if not value in [tz.lower() for tz in pytz.all_timezones]:
            raise ValueError(f"{ERROR_COLOR}Timezone must be valid IANA timezone identifier (https://en.wikipedia.org/wiki/List_of_tz_database_time_zones){Style.RESET_ALL}")
        normalized_value = pytz.all_timezones[[tz.lower() for tz in pytz.all_timezones].index(value)]
        timestamp["timezone"] = normalized_value
        self.config['rename']['timestamp'] = timestamp
        self._print_set_message("Timestamp Timezone", normalized_value, 'rename')
        return self
    def set_rename_timestamp_position(self, value):
        timestamp = self._create_or_get_timestamp()
        if not value or len(value) < 1:
            timestamp["position"] = None
            return
        if value not in [TimestampPosition.START.value, TimestampPosition.AFTER_PREFIX.value, TimestampPosition.BEFORE_SUFFIX.value, TimestampPosition.END.value]:
            raise ValueError(f"{ERROR_COLOR}Invalid position: {value}. Must be one of {TimestampPosition.START.value}, {TimestampPosition.AFTER_PREFIX.value}, {TimestampPosition.BEFORE_SUFFIX.value}, {TimestampPosition.END.value}{Style.RESET_ALL}")
        timestamp["position"] = value
        self.config['rename']['timestamp'] = timestamp
        self._print_set_message("Timestamp Position", value, 'rename')
        return self

    def set_source_directory(self, value):
        self._validate_path(value)
        self.config['source_directory'] = value
        self._print_set_message("Source Directory", value)
        return self
    def set_source_directories(self, values):
        for source in values:
            self._validate_path(source)
        self.config['source_directories'] = values
        self._print_set_message("Source Directories", values)
        return self

    def set_destination_directory(self, value):
        self._validate_path(value)
        self.config['destination_directory'] = value
        self._print_set_message("Destination Directory", value)
        return self
    def set_destination_directories(self, values):
        for destination in values:
            self._validate_path(destination)
        self.config['destination_directories'] = values
        self._print_set_message("Destination Directories", values)
        return self
    
    def set_file_type(self, value):
        if not value.isalnum():
            raise ValueError(f"{ERROR_COLOR}File type must be alphanumeric{Style.RESET_ALL}")
        self.config['file_type'] = value
        self._print_set_message("File Type", value)
        return self
    def set_file_types(self, values):
        for value in values:
            if not value.isalnum():
                raise ValueError(f"{ERROR_COLOR}File type must be alphanumeric{Style.RESET_ALL}")
        self.config['file_types'] = values
        self._print_set_message("File Types", values)
        return self
    def set_file_type_regex(self, value):
        if not self._is_valid_regex(value):
            raise ValueError(f"{ERROR_COLOR}Regex file type must be a valid regular expression{Style.RESET_ALL}")
        self.config['file_type_regex'] = value
        self._print_set_message("File Type Regex", value)
        return self
    def set_file_type_exclude_regex(self, value):
        if not self._is_valid_regex(value):
            raise ValueError(f"{ERROR_COLOR}Regex exclude file type must be a valid regular expression{Style.RESET_ALL}")
        self.config['file_type_exclude_regex'] = value
        self._print_set_message("File Type Exclude Regex", value)
        return self

    def set_file_name(self, value):
        if len(value) < 1:
            raise ValueError(f"{ERROR_COLOR}File name must not be blank{Style.RESET_ALL}")
        self.config['file_name'] = value
        self._print_set_message("File Name", value)
        return self
    def set_file_names(self, values):
        for value in values:
            if len(value) < 1:
                raise ValueError(f"{ERROR_COLOR}File name must not be blank{Style.RESET_ALL}")
        self.config['file_names'] = values
        self._print_set_message("File Names", values)
        return self
    def set_file_name_contains(self, value):
        if len(value) < 1:
            raise ValueError(f"{ERROR_COLOR}File name contains must not be blank{Style.RESET_ALL}")
        self.config['file_name_contains'] = value
        self._print_set_message("File Name Contains", value)
        return self
    def set_file_name_starts_with(self, value):
        if len(value) < 1:
            raise ValueError(f"{ERROR_COLOR}File name starts with must not be blank{Style.RESET_ALL}")
        self.config['file_name_starts_with'] = value
        self._print_set_message("File Name Starts With", value)
        return self
    def set_file_name_ends_with(self, value):
        if len(value) < 1:
            raise ValueError(f"{ERROR_COLOR}File name ends with must not be blank{Style.RESET_ALL}")
        self.config['file_name_ends_with'] = value
        self._print_set_message("File Name Ends With", value)
        return self
    def set_file_name_regex(self, value):
        if not self._is_valid_regex(value):
            raise ValueError(f"{ERROR_COLOR}Regex file name must be a valid regular expression{Style.RESET_ALL}")
        self.config['file_name_regex'] = value
        self._print_set_message("File Name Regex", value)
        return self
    def set_file_name_exclude_regex(self, value):
        if not self._is_valid_regex(value):
            raise ValueError(f"{ERROR_COLOR}Regex exclude file name must be a valid regular expression{Style.RESET_ALL}")
        self.config['file_name_exclude_regex'] = value
        self._print_set_message("File Name Exclude Regex", value)
        return self

    def set_recursive(self, value):
        if not isinstance(value, bool):
            raise ValueError(f"{ERROR_COLOR}Recursive must be a boolean value{Style.RESET_ALL}")
        self.config['recursive'] = value
        self._print_set_message("Recursive", value)
        return self
    def set_keep_source(self, value):
        if not isinstance(value, bool):
            raise ValueError(f"{ERROR_COLOR}Keep Source must be a boolean value{Style.RESET_ALL}")
        self.config['keep_source'] = value
        self._print_set_message("Keep Source", value)
        return self

    def set_name(self, value):
        if not value or len(value) < 1:
            raise ValueError(f"{ERROR_COLOR}Name must not be blank{Style.RESET_ALL}")
        self.config['name'] = value
        self._print_set_message("Name", value)
        return self
    def set_description(self, value):
        self.config['description'] = value
        self._print_set_message("Description", value)
        return self

    def save_config(self, path):
        self._validate_path(path)
        if os.path.exists(path):
            raise ValueError(f"{ERROR_COLOR}A file already exists at {path}. Overwriting files is disabled to avoid accidental data loss{Style.RESET_ALL}")
        with open(path, 'w') as f:
            json.dump(self.config, f, indent=4, default=str)
        print(f"{Fore.GREEN}Configuration saved to {path}{Style.RESET_ALL}")
#===========================================================


class InteractiveMoverConfigBuilder(MoverConfigBuilder):
#=====Input/Output Helpers==================================
    def _repeat_prompt_until_valid(self, prompt_func, input_condition=lambda x: True, invalid_message=None, *args):
        while True:
            try:
                result = prompt_func(*args)
                if input_condition(result):
                    return result
                else:
                    if invalid_message:
                        print(f"{ERROR_COLOR}{invalid_message}{Style.RESET_ALL}")
                    else:
                        print(f"{ERROR_COLOR}Invalid input{Style.RESET_ALL}")
            except ValueError as e:
                print(e)

    def _get_menu_text(self, prompt, options):
        menu = f"{prompt}{Style.RESET_ALL}\n"
        for key, value in options.items():
            menu += f" [{MENU_OPTION_VALUE_COLOR}{key}{Style.RESET_ALL}] {MENU_OPTION_NAME_COLOR}{value}{Style.RESET_ALL}\n"
        return menu
#===========================================================

    # ===== Source Directory =====
    def _interactive_source_directory(self):
        option_map = {'0': False, '1': True}
        self.multiple_sources = option_map.get(self._repeat_prompt_until_valid(
            lambda: input(self._get_menu_text(f"Select your {PARAMETER_COLOR}source directory mode{Style.RESET_ALL}:", {'0': 'Single Directory', '1': 'Multiple Directory'})).strip().lower(),
            input_condition=lambda x: x in ['0', '1'],
            invalid_message="Please enter a valid menu option"
        ))

        if self.multiple_sources:
            self.config['source_directories'] = []
            while True:
                source = self._repeat_prompt_until_valid(
                    lambda: input(f"Enter {PARAMETER_COLOR}source directory{Style.RESET_ALL} (or 'done' to finish): ").strip(),
                    input_condition=lambda x: x.lower() == 'done' or self._is_valid_path(x),
                    invalid_message="Please enter a valid absolute path or 'done'"
                )
                if source.lower() == 'done':
                    if not self.config['source_directories']:
                        print(f"{ERROR_COLOR}At least one source directory must be specified{Style.RESET_ALL}")
                        continue
                    break
                self.config['source_directories'].append(source)
            print(f"{Fore.GREEN}Added source directories:{Style.RESET_ALL}")
            for source in self.config['source_directories']:
                print(f"{SET_VALUE_COLOR}- {source}{Style.RESET_ALL}")
        else:
            self._repeat_prompt_until_valid(
                lambda: input(f"Enter {PARAMETER_COLOR}source directory{Style.RESET_ALL}: ").strip(),
                input_condition=lambda x: self._try_set_option('source_directory', x),
                invalid_message="Please enter a valid absolute path"
            )

    # ===== Destination Directory =====
    def _interactive_destination_directory(self):
        menu_option = self._repeat_prompt_until_valid(
            lambda: input(self._get_menu_text(f"Select your {PARAMETER_COLOR}destination directory mode{Style.RESET_ALL}:", {'0': 'Single Directory', '1': 'Multiple Directory'})).strip().lower(),
            input_condition=lambda x: x in ['0', '1'],
            invalid_message="Please enter a valid menu option"
        )
        self.multiple_destinations = menu_option == '1'
        if self.multiple_destinations:
            self.config['destination_directories'] = []
            while True:
                destination = self._repeat_prompt_until_valid(
                    lambda: input(f"Enter {PARAMETER_COLOR}destination directory{Style.RESET_ALL} (or 'done' to finish): ").strip(),
                    input_condition=lambda x: x.lower() == 'done' or self._is_valid_path(x),
                    invalid_message="Please enter a valid absolute path or 'done'"
                )
                if destination.lower() == 'done':
                    if not self.config['destination_directories']:
                        print(f"{ERROR_COLOR}At least one destination directory must be specified{Style.RESET_ALL}")
                        continue
                    break
                self.config['destination_directories'].append(destination)
            print(f"{Fore.GREEN}Added destination directories:{Style.RESET_ALL}")
            for destination in self.config['destination_directories']:
                print(f"{VALUE_COLOR}- {destination}{Style.RESET_ALL}")
        else:
            self._repeat_prompt_until_valid(
                lambda: input(f"Enter {PARAMETER_COLOR}destination directory{Style.RESET_ALL}: ").strip(),
                input_condition=lambda x: self._try_set_option('destination_directory', x),
                invalid_message="Please enter a valid absolute path"
            )

    # ===== Filters =====
    def _interactive_file_type_filter(self):
        menu_option = self._repeat_prompt_until_valid(
            lambda: input(self._get_menu_text(f"Which kind of {PARAMETER_COLOR}file type filter{Style.RESET_ALL} would you like to configure?", {'0': 'Single File Type', '1': 'Multiple File Types', '2': 'Regex (include)', '3': 'Regex (exclude)', '4': 'Cancel (return to filter menu)'})).strip().lower(),
            input_condition=lambda x: x in ['0', '1', '2', '3', '4'],
            invalid_message="Please enter a valid menu option"
        )
        if menu_option == '0':
            # Single File Type
            continue_update = True
            override_multi = False
            update_multi = False
            if 'file_type' in self.config:
                menu_option = self._repeat_prompt_until_valid(
                    lambda: input(self._get_menu_text(f"{WARNING_COLOR}You previously defined a {PARAMETER_COLOR}Single File Type{Style.RESET_ALL}{WARNING_COLOR} filter. Would you like to override it?{Style.RESET_ALL}", {'0': 'No (cancel)', '1': 'Yes'})).strip().lower(),
                    input_condition=lambda x: x in ['0', '1'],
                    invalid_message="Please enter a valid menu option"
                )
                if menu_option == '1':
                    continue_update = True
                elif menu_option == '0':
                    continue_update = False
            if 'file_types' in self.config:
                
                menu_option = self._repeat_prompt_until_valid(
                    lambda: input(self._get_menu_text(f"{WARNING_COLOR}You previously defined a {PARAMETER_COLOR}Multiple File Type{Style.RESET_ALL}{WARNING_COLOR} filter. How would you like to proceed?{Style.RESET_ALL}", {'0': 'Override it', '1': 'Add to it', '2': 'Cancel'})).strip().lower(),
                    input_condition=lambda x: x in ['0', '1', '2'],
                    invalid_message="Please enter a valid menu option"
                )
                if menu_option == '0':
                    continue_update = True
                    override_multi = True
                elif menu_option == '1':
                    continue_update = True
                    update_multi = True
                elif menu_option == '2':
                    continue_update = False

            if continue_update:
                file_type = self._repeat_prompt_until_valid(
                    lambda: input(f"Enter a {PARAMETER_COLOR}file type{Style.RESET_ALL} (without the preceding '.'): ").strip().lower(),
                    input_condition=lambda x: x.isalnum(),
                    invalid_message="Please enter a valid file type (alphanumeric characters only, no spaces or dots)"
                )
                if override_multi:
                    self.config.pop('file_types', None)
                    self.config['file_type'] = file_type
                    self._print_set_message("File Type", file_type)
                elif update_multi:
                    self.config['file_types'].append(file_type)
                    self._print_set_message("File Types", self.config['file_types'])
                else:
                    self.config['file_type'] = file_type
                    self._print_set_message("File Type", file_type)
        elif menu_option == '1':
            # Multiple File Type
            continue_update = True
            override_single = False
            update_single = False
            override_multi = False
            update_multi = False
            if 'file_types' in self.config:
                menu_option = self._repeat_prompt_until_valid(
                    lambda: input(self._get_menu_text(f"{WARNING_COLOR}You previously defined a {PARAMETER_COLOR}Multiple File Type Filter{Style.RESET_ALL}{WARNING_COLOR}. How would you like to proceed?{Style.RESET_ALL}", {'0': 'Override it', '1': 'Add to it', '2': 'Cancel'})).strip().lower(),
                    input_condition=lambda x: x in ['0', '1', '2'],
                    invalid_message="Please enter a valid menu option"
                )
                if menu_option == '0':
                    continue_update = True
                    override_multi = True
                elif menu_option == '1':
                    continue_update = True
                    update_multi = True
                elif menu_option == '2':
                    continue_update = False
            if 'file_type' in self.config:
                
                menu_option = self._repeat_prompt_until_valid(
                    lambda: input(self._get_menu_text(f"{WARNING_COLOR}You previously defined a {PARAMETER_COLOR}Single File Type Filter{Style.RESET_ALL}{WARNING_COLOR}. How would you like to proceed?{Style.RESET_ALL}", {'0': 'Override it', '1': 'Add to it', '2': 'Cancel'})).strip().lower(),
                    input_condition=lambda x: x in ['0', '1', '2'],
                    invalid_message="Please enter a valid menu option"
                )
                if menu_option == '0':
                    continue_update = True
                    override_single = True
                elif menu_option == '1':
                    continue_update = True
                    update_single = True
                elif menu_option == '2':
                    continue_update = False
            if continue_update:
                if override_multi or not update_multi:
                    self.config['file_types'] = []
                if override_single:
                    self.config.pop('file_type', None)
                if update_single:
                    self.config['file_types'].append(self.config['file_type'])
                    self.config.pop('file_type', None)

                while True:
                    file_type = self._repeat_prompt_until_valid(
                        lambda: input(f"Enter a {PARAMETER_COLOR}file type{Style.RESET_ALL} (without the preceding '.') or 'done' to finish: ").strip().lower(),
                        input_condition=lambda x: x.isalnum(),
                        invalid_message="Please enter a valid file type (alphanumeric characters only, no spaces or dots)"
                    )
                    if file_type == 'done':
                        if not len(self.config['file_types']) > 0:
                            print(f"{ERROR_COLOR}At least one file type must be specified{Style.RESET_ALL}")
                            continue
                        break
                    elif file_type in self.config['file_types']:
                        print(f"{VALUE_COLOR}{file_type}{Style.RESET_ALL} already included in {PARAMETER_COLOR}file types{Style.RESET_ALL}")
                    else:
                        self.config['file_types'].append(file_type)
                self._print_set_message("File Types", self.config['file_types'])
                
        elif menu_option == '2':
            # Regex (include) File Type
            self._repeat_prompt_until_valid(
                lambda: input(f"Enter a regular expression to match {PARAMETER_COLOR}file type{Style.RESET_ALL}: ").strip().lower(),
                input_condition=lambda x: self._try_set_option('file_type_regex', x),
                invalid_message="The specified input is not a valid regular expression"
            )
        elif menu_option == '3':
            # Regex (exclude) File Type
            self._repeat_prompt_until_valid(
                lambda: input(f"Enter a regular expression to exclude {PARAMETER_COLOR}file type{Style.RESET_ALL}: ").strip().lower(),
                input_condition=lambda x: self._try_set_option('file_type_exclude_regex', x),
                invalid_message="The specified input is not a valid regular expression"
            )
        elif menu_option == '4':
            return
    def _interactive_file_name_filter(self):
        menu_option = self._repeat_prompt_until_valid(
            lambda: input(self._get_menu_text(f"Which kind of {PARAMETER_COLOR}file name filter{Style.RESET_ALL} would you like to configure?", {'0': 'Single Exact Name', '1': 'Multiple Exact Names', '2': 'Contains', '3': 'Starts With', '4': 'Ends With', '5': 'Regex (include)', '6': 'Regex (exclude)', '7': 'Cancel (return to filter menu)'})).strip().lower(),
            input_condition=lambda x: x in ['0', '1', '2', '3', '4', '5', '6', '7'],
            invalid_message="Please enter a valid menu option"
        )
        if menu_option == '0':
            # Single Exact Name
            continue_update = True
            override_multi = False
            update_multi = False
            if 'file_name' in self.config:
                
                menu_option = self._repeat_prompt_until_valid(
                    lambda: input(self._get_menu_text(f"{WARNING_COLOR}You previously defined a {PARAMETER_COLOR}Single File Name{Style.RESET_ALL}{WARNING_COLOR} filter. Would you like to override it?{Style.RESET_ALL}", {'0': 'No (cancel)', '1': 'Yes'})).strip().lower(),
                    input_condition=lambda x: x in ['0', '1'],
                    invalid_message="Please enter a valid menu option"
                )
                if menu_option == '1':
                    continue_update = True
                elif menu_option == '0':
                    continue_update = False
            if 'file_names' in self.config:
                
                menu_option = self._repeat_prompt_until_valid(
                    lambda: input(self._get_menu_text(f"{WARNING_COLOR}You previously defined a {PARAMETER_COLOR}Multiple File Name{Style.RESET_ALL}{WARNING_COLOR} filter. How would you like to proceed?{Style.RESET_ALL}", {'0': 'Override it', '1': 'Add to it', '2': 'Cancel'})).strip().lower(),
                    input_condition=lambda x: x in ['0', '1', '2'],
                    invalid_message="Please enter a valid menu option"
                )
                if menu_option == '0':
                    continue_update = True
                    override_multi = True
                elif menu_option == '1':
                    continue_update = True
                    update_multi = True
                elif menu_option == '2':
                    continue_update = False

            if continue_update:
                file_name = self._repeat_prompt_until_valid(
                    lambda: input(f"Enter a {PARAMETER_COLOR}file name{Style.RESET_ALL} {Fore.BLACK}(note: do not include a file type extension - it will not be matched by this filter){Style.RESET_ALL}: ").strip().lower(),
                    input_condition=lambda x: len(x) > 0,
                    invalid_message="Please enter a valid file name"
                )
                if override_multi:
                    self.config.pop('file_names', None)
                    self.config['file_name'] = file_name
                    self._print_set_message("File Name", file_name)
                elif update_multi:
                    self.config['file_names'].append(file_name)
                    self._print_set_message("File Names", self.config['file_names'])
                else:
                    self.config['file_name'] = file_name
                    self._print_set_message("File Name", file_name)
                
        elif menu_option == '1':
            # Multiple Exact Name
            continue_update = True
            override_single = False
            update_single = False
            override_multi = False
            update_multi = False
            if 'file_names' in self.config:
                menu_option = self._repeat_prompt_until_valid(
                    lambda: input(self._get_menu_text(f"{WARNING_COLOR}You previously defined a {PARAMETER_COLOR}Multiple File Name{Style.RESET_ALL}{WARNING_COLOR} filter. How would you like to proceed?{Style.RESET_ALL}", {'0': 'Override it', '1': 'Add to it', '2': 'Cancel'})).strip().lower(),
                    input_condition=lambda x: x in ['0', '1', '2'],
                    invalid_message="Please enter a valid menu option"
                )
                if menu_option == '0':
                    continue_update = True
                    override_multi = True
                elif menu_option == '1':
                    continue_update = True
                    update_multi = True
                elif menu_option == '2':
                    continue_update = False
            if 'file_name' in self.config:
                menu_option = self._repeat_prompt_until_valid(
                    lambda: input(self._get_menu_text(f"{WARNING_COLOR}You previously defined a {PARAMETER_COLOR}Single File Name{Style.RESET_ALL}{WARNING_COLOR} filter. How would you like to proceed?{Style.RESET_ALL}", {'0': 'Override it', '1': 'Add to it', '2': 'Cancel'})).strip().lower(),
                    input_condition=lambda x: x in ['0', '1', '2'],
                    invalid_message="Please enter a valid menu option"
                )
                if menu_option == '0':
                    continue_update = True
                    override_single = True
                elif menu_option == '1':
                    continue_update = True
                    update_single = True
                elif menu_option == '2':
                    continue_update = False
            if continue_update:
                if override_multi or not update_multi:
                    self.config['file_names'] = []
                if override_single:
                    self.config.pop('file_name', None)
                if update_single:
                    self.config['file_names'].append(self.config['file_name'])
                    self.config.pop('file_name', None)

                while True:
                    file_name = self._repeat_prompt_until_valid(
                        lambda: input(f"Enter a {PARAMETER_COLOR}file name{Style.RESET_ALL} (without the file type extension) or 'done' to finish: ").strip().lower(),
                        input_condition=lambda x: len(x) > 0,
                        invalid_message="Please enter a valid file name"
                    )
                    if file_name == 'done':
                        if not len(self.config['file_names']) > 0:
                            print(f"{ERROR_COLOR}At least one file name must be specified{Style.RESET_ALL}")
                            continue
                        break
                    elif file_name in self.config['file_names']:
                        print(f"{VALUE_COLOR}{file_name}{Style.RESET_ALL} already included in {PARAMETER_COLOR}file names{Style.RESET_ALL}")
                    else:
                        self.config['file_names'].append(file_name)
                self._print_set_message("File Names", self.config['file_names'])
                
        elif menu_option == '2':
            # Contains
            self._repeat_prompt_until_valid(
                lambda: input(f"Enter a substring to match within a {PARAMETER_COLOR}file name{Style.RESET_ALL} (without the file type extension): ").strip().lower(),
                input_condition=lambda x: self._try_set_option('file_name_contains', x),
                invalid_message="Please enter a valid file name substring"
            )
        elif menu_option == '3':
            # Starts With
            self._repeat_prompt_until_valid(
                lambda: input(f"Enter a substring to match the start of a {PARAMETER_COLOR}file name{Style.RESET_ALL}: ").strip().lower(),
                input_condition=lambda x: self._try_set_option('file_name_starts_with', x),
                invalid_message="Please enter a valid file name substring"
            )
        elif menu_option == '4':
            # Ends With
            self._repeat_prompt_until_valid(
                lambda: input(f"Enter a substring to match the end of a {PARAMETER_COLOR}file name{Style.RESET_ALL} (without the file type extension): ").strip().lower(),
                input_condition=lambda x: self._try_set_option('file_name_ends_with', x),
                invalid_message="Please enter a valid file name substring"
            )
        elif menu_option == '5':
            # Regex (include)
            self._repeat_prompt_until_valid(
                lambda: input(f"Enter a regex pattern to match files by {PARAMETER_COLOR}file name{Style.RESET_ALL}: ").strip().lower(),
                input_condition=lambda x: self._try_set_option('file_name_regex', x),
                invalid_message="The specified input is not a valid regular expression"
            )
            
        elif menu_option == '6':
            # Regex (exclude)
            self._repeat_prompt_until_valid(
                lambda: input(f"Enter a regex pattern to exclude files by {PARAMETER_COLOR}file name{Style.RESET_ALL}: ").strip().lower(),
                input_condition=lambda x: self._try_set_option('file_name_exclude_regex', x),
                invalid_message="The specified input is not a valid regular expression"
            )
        elif menu_option == '7':
            return
    def _interactive_filters(self):
        has_file_type_filter = False
        has_name_filter = False
        while True:
            menu_option = self._repeat_prompt_until_valid(
                lambda: input(self._get_menu_text(f"Select a {PARAMETER_COLOR}file filter mode{Style.RESET_ALL} to configure (you will have the chance to define multiple):", {'0': 'File Type', '1': 'File Name', '2': 'Done / Apply All Filters'})).strip().lower(),
                input_condition=lambda x: x in ['0', '1', '2'],
                invalid_message="Please enter a valid menu option"
            )
            if menu_option == '0':
                self._interactive_file_type_filter()
                has_file_type_filter = True
            elif menu_option == '1':
                self._interactive_file_name_filter()
                has_name_filter = True
            elif menu_option == '2':
                if not has_file_type_filter and not has_name_filter:
                    
                    menu_option = self._repeat_prompt_until_valid(
                        lambda: input(self._get_menu_text(f"{ERROR_COLOR}Neither a file type nor file name filter has been defined. This will match ALL files in the source directory. Is this correct?{Style.RESET_ALL}", {'0': 'No', '1': 'Yes'})).strip().lower(),
                        input_condition=lambda x: x in ['0', '1'],
                        invalid_message="Please enter a valid menu option"
                    )
                    if menu_option == '1':
                        return
                    else:
                        continue
                return

    # ===== Keep Source =====
    def _interactive_keep_source(self):
        option_map = {'0': False, '1': True}
        
        self._repeat_prompt_until_valid(
            lambda: input(self._get_menu_text(f"After the file move(s) are done, do you want to keep the source file or remove it?", {'0': 'Keep Source', '1': 'Remove Source'})).strip().lower(),
            input_condition=lambda x: self._try_set_option('keep_source', option_map.get(x)),
            invalid_message="Please enter a valid menu option"
        )

    # ===== Recursive =====
    def _interactive_recursive(self):
        option_map = {'0': False, '1': True}
        
        self._repeat_prompt_until_valid(
            lambda: input(self._get_menu_text(f"Should file matching be recursive (i.e., traverse any subdirectories in the source directory to find matches)?", {'0': 'No', '1': 'Yes'})).strip().lower(),
            input_condition=lambda x: self._try_set_option('recursive', option_map.get(x)),
            invalid_message="Please enter a valid menu option"
        )

    # ===== Name =====
    def _interactive_name(self):
        self._repeat_prompt_until_valid(
            lambda: input(f"Enter a name for your file mover (a short identifier): ").strip().lower(),
            input_condition=lambda x: self._try_set_option('name', x),
            invalid_message="Please enter a valid string"
        )

    # ===== Description =====
    def _interactive_description(self):
        self._repeat_prompt_until_valid(
            lambda: input(f"Enter a description for your file mover (optional): ").strip().lower(),
            input_condition=lambda x: self._try_set_option('description', x)
        )

    # ===== Rename Configuration =====
    def _interactive_timestamp_config(self):
        menu_option = self._repeat_prompt_until_valid(
            lambda: input(self._get_menu_text(f"Should a {PARAMETER_COLOR}timestamp{Style.RESET_ALL} be added to moved files?", {'0': 'No', '1': 'Yes'})).strip().lower(),
            input_condition=lambda x: x in ['0', '1'],
            invalid_message="Please enter a valid menu option"
        )
        if menu_option == '0':
            return
        self._repeat_prompt_until_valid(
            lambda: input(f"(Optional) Enter the {PARAMETER_COLOR}timestamp format{Style.RESET_ALL} {Fore.BLACK}(e.g., yyyy-MM-dd_HH-mm-ss){Style.RESET_ALL} (leave blank for default): ").strip().lower(),
            input_condition=lambda x: self._try_set_timestamp_option('format', x),
            invalid_message=None
        )
        self._repeat_prompt_until_valid(
            lambda: input(f"(Optional) Enter the {PARAMETER_COLOR}timestamp IANA Timezone Identifier{Style.RESET_ALL} {Fore.BLACK}Refer to https://en.wikipedia.org/wiki/List_of_tz_database_time_zones for a list of accepted values{Style.RESET_ALL}. (leave blank for default): ").strip().lower(),
            input_condition=lambda x: self._try_set_timestamp_option('timezone', x),
            invalid_message=None
        )
        
        option_map = {'0': TimestampPosition.START.value, '1': TimestampPosition.AFTER_PREFIX.value, '2': TimestampPosition.BEFORE_SUFFIX.value, '3': TimestampPosition.END.value}
        
        menu_option = self._repeat_prompt_until_valid(
            lambda: input(self._get_menu_text(f"Select the {PARAMETER_COLOR}position{Style.RESET_ALL} the timestamp should be placed:", {'0': 'Start', '1': 'After Prefix', '2': 'Before Suffix', '3': 'End'})).strip().lower(),
            input_condition=lambda x: self._try_set_timestamp_option('position', option_map.get(x)),
            invalid_message=None
        )

    def _interactive_rename_config(self):
        menu_option = self._repeat_prompt_until_valid(
            lambda: input(self._get_menu_text(f"Would you like to configure {PARAMETER_COLOR}renaming files{Style.RESET_ALL} when they're moved?", {'0': 'No', '1': 'Yes'})).strip().lower(),
            input_condition=lambda x: x in ['0', '1'],
            invalid_message="Please enter a valid menu option"
        )
        if menu_option == '0':
            return
        
        # Case sensitive
        
        menu_option = self._repeat_prompt_until_valid(
            lambda: input(self._get_menu_text(f"Should rename replace matching rules be {PARAMETER_COLOR}case sensitive{Style.RESET_ALL}?", {'0': 'No', '1': 'Yes'})).strip().lower(),
            input_condition=lambda x: x in ['0', '1'],
            invalid_message="Please enter a valid menu option"
        )
        if menu_option == '1':
            self.set_rename_case_sensitive(True)
        elif menu_option == '0':
            self.set_rename_case_sensitive(False)
        
        # Prefix
        self._repeat_prompt_until_valid(
            lambda: input(f"(Optional) Enter a {PARAMETER_COLOR}prefix{Style.RESET_ALL} to match files to rename: ").strip().lower(),
            input_condition=lambda x: self._try_set_rename_option('prefix', x),
            invalid_message=None
        )
        # Suffix
        self._repeat_prompt_until_valid(
            lambda: input(f"(Optional) Enter a {PARAMETER_COLOR}suffix{Style.RESET_ALL} to match files to rename: ").strip().lower(),
            input_condition=lambda x: self._try_set_rename_option('suffix', x),
            invalid_message=None
        )

        while True:
            menu_option = self._repeat_prompt_until_valid(
                lambda: input(self._get_menu_text(f"Add a {PARAMETER_COLOR}text replace rule{Style.RESET_ALL}? You may define 0 or more", {'0': 'Add Rule', '1': 'Done'})).strip().lower(),
                input_condition=lambda x: x in ['0', '1'],
                invalid_message="Please enter a valid menu option"
            )
            if menu_option == '1':
                break
            search = self._repeat_prompt_until_valid(
                lambda: input(f"Enter the text to {PARAMETER_COLOR}search/match{Style.RESET_ALL}: ").strip().lower(),
                input_condition=lambda x: len(x) > 0,
                invalid_message="Search cannot be blank"
            )
            replace = self._repeat_prompt_until_valid(
                lambda: input(f"Enter the text to {PARAMETER_COLOR}replace{Style.RESET_ALL} the matched text in search with: ").strip().lower()
            )
            try:
                self.add_replace_rule({"search": search, "replace": replace})
            except ValueError as e:
                print(e)
        
        self._interactive_timestamp_config()

    def _interactive_save_config(self):
        menu_option = self._repeat_prompt_until_valid(
            lambda: input(self._get_menu_text(f"How would you like to save this configuration?", {'0': 'Print as Text', '1': 'Save to File', '2': 'Do Nothing'})).strip().lower(),
            input_condition=lambda x: x in ['0', '1', '2'],
            invalid_message="Please enter a valid menu option"
        )
        if menu_option == '2':
            return
        if menu_option == '0':
            print(f"{Fore.GREEN}Configuration complete! Here is the resulting configuration:{Style.RESET_ALL}")
            print(json.dumps(self.config, indent=4, default=str))
        while True:
            file_path = self._repeat_prompt_until_valid(
                lambda: input(f"Enter the absolute path of the file to save the configuration to {Fore.BLACK}(including .json extension){Style.RESET_ALL}: ").strip(),
                input_condition=lambda x: self._is_valid_path(x) and x.lower().endswith('.json'),
                invalid_message="Please enter a valid absolute path ending with .json"
            )
            try:
                self.save_config(file_path)
                break
            except Exception as e:
                print(f"{ERROR_COLOR}Failed to save configuration: {e}{Style.RESET_ALL}")

    def interactive_build(self):
        print(f"{Fore.LIGHTMAGENTA_EX}============================================================" \
              f"\n\n" \
              f"{Fore.LIGHTWHITE_EX}           Interactive File Mover Config Builder" \
              f"\n{Fore.LIGHTBLACK_EX}" \
              f"-> Follow the prompts to create the configuration for a new\n" \
              f"   File Mover" \
              f"\n" \
              f"-> Once complete, you can use it in a new FileMover object\n"
              f"   to perform your file moving actions as configured!"
              f"\n\n" \
              f"{Fore.LIGHTMAGENTA_EX}============================================================{Style.RESET_ALL}\n")
        input(f"Press Enter to begin...")
        print()
        self._interactive_source_directory()
        self._interactive_destination_directory()

        self._interactive_filters()
        
        self._interactive_rename_config()
        self._interactive_keep_source()
        self._interactive_recursive()

        self._interactive_name()
        self._interactive_description()
        self._interactive_save_config()
        return self.config

from src.filemover.rename_config import TimestampPosition

from colorama import Fore, Style
import os
import pytz

SET_INFO_COLOR = Fore.LIGHTBLACK_EX
SET_PARAMETER_COLOR = Fore.LIGHTCYAN_EX
SET_VALUE_COLOR = Fore.LIGHTYELLOW_EX
MENU_OPTION_VALUE_COLOR = Fore.MAGENTA
MENU_OPTION_NAME_COLOR = Fore.BLUE


class InteractiveMoverConfigBuilder:
    def __init__(self):
        self.multiple_sources = False
        self.multiple_destinations = False
        self.config = {}

    def _validate_path(self, path):
        if not path or not path.strip():
            raise ValueError(f"{Fore.RED}Path cannot be empty{Style.RESET_ALL}")
        if not isinstance(path, str):
            raise ValueError(f"{Fore.RED}Path must be a string{Style.RESET_ALL}")
        if not os.path.isabs(path):
            raise ValueError(f"{Fore.RED}Path must be an absolute path{Style.RESET_ALL}")

    def _is_valid_path(self, path):
        if not path or not path.strip():
            return False
        if not isinstance(path, str):
            return False
        if not os.path.isabs(path):
            return False
        return True
    
    def _try_set_option(self, option, value):
        try:
            if option == 'source_directory':
                self.set_source(value)
            elif option == 'source_directories':
                self.set_sources(value)
            elif option == 'destination_directory':
                self.set_destination(value)
            elif option == 'destination_directories':
                self.set_destinations(value)
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
                raise ValueError(f"{Fore.RED}Unknown config option '{option}'")
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
                raise ValueError(f"{Fore.RED}Unknown rename config option '{option}'")
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
                raise ValueError(f"{Fore.RED}Unknown rename timestamp config option '{option}'")
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

    def _print_set_message(self, option, value, value_detail = None):
        print(f"{SET_INFO_COLOR}Set {f'{value_detail} ' if value_detail else ''}{SET_PARAMETER_COLOR}{option}{Style.RESET_ALL}{SET_INFO_COLOR} to {SET_VALUE_COLOR}{value}{Style.RESET_ALL}\n")

    def set_rename_case_sensitive(self, value):
        if not isinstance(value, bool):
            raise ValueError(f"{Fore.RED}Case Sensitive must be a boolean value{Style.RESET_ALL}")
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
            raise ValueError(f"{Fore.RED}Search must not be blank in replace rule{Style.RESET_ALL}")
        if not 'replace' in value:
            value['replace'] = ""
        
        rename = self._create_or_get_rename()
        if 'replace' not in rename:
            rename['replace'] = []
        rename['replace'].append(value)
        self.config['rename'] = rename
        print(f"{SET_INFO_COLOR}Added rename Replace Rule: {SET_PARAMETER_COLOR}Search{Style.RESET_ALL}{SET_INFO_COLOR}: {SET_VALUE_COLOR}{value['search']}{Style.RESET_ALL}{SET_INFO_COLOR}, Replace: {SET_VALUE_COLOR}{value['replace'] if len(value['replace']) > 0 else f'{Fore.RED}<REMOVE>{Style.RESET_ALL}'}{Style.RESET_ALL}")
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
        if not value in pytz.all_timezones:
            raise ValueError(f"{Fore.RED}Timezone must be a valid timezone{Style.RESET_ALL}")
        timestamp["timezone"] = value
        self.config['rename']['timestamp'] = timestamp
        self._print_set_message("Timestamp Timezone", value, 'rename')
        return self
    def set_rename_timestamp_position(self, value):
        timestamp = self._create_or_get_timestamp()
        if not value or len(value) < 1:
            timestamp["position"] = None
            return
        if value not in [TimestampPosition.START.value, TimestampPosition.AFTER_PREFIX.value, TimestampPosition.BEFORE_SUFFIX.value, TimestampPosition.END.value]:
            raise ValueError(f"{Fore.RED}Invalid position: {value}. Must be one of {TimestampPosition.START.value}, {TimestampPosition.AFTER_PREFIX.value}, {TimestampPosition.BEFORE_SUFFIX.value}, {TimestampPosition.END.value}{Style.RESET_ALL}")
        timestamp["position"] = value
        self.config['rename']['timestamp'] = timestamp
        self._print_set_message("Timestamp Position", value, 'rename')
        return self
        


    def set_source(self, value):
        self._validate_path(value)
        self.config['source_directory'] = value
        self._print_set_message("Source Directory", value)
        return self
    def set_sources(self, values):
        for source in values:
            self._validate_path(source)
        self.config['source_directories'] = values
        self._print_set_message("Source Directories", values)
        return self

    def set_destination(self, value):
        self._validate_path(value)
        self.config['destination_directory'] = value
        self._print_set_message("Destination Directory", value)
        return self
    def set_destinations(self, values):
        for destination in values:
            self._validate_path(destination)
        self.config['destination_directories'] = values
        self._print_set_message("Destination Directories", values)
        return self
    
    def set_file_type(self, value):
        if not value.isalnum():
            raise ValueError(f"{Fore.RED}File type must be alphanumeric{Style.RESET_ALL}")
        self.config['file_type'] = value
        self._print_set_message("File Type", value)
        return self
    def set_file_types(self, values):
        for value in values:
            if not value.isalnum():
                raise ValueError(f"{Fore.RED}File type must be alphanumeric{Style.RESET_ALL}")
        self.config['file_types'] = values
        self._print_set_message("File Types", values)
        return self
    def set_file_type_regex(self, value):
        if not self._is_valid_regex(value):
            raise ValueError(f"{Fore.RED}Regex file type must be a valid regular expression{Style.RESET_ALL}")
        self.config['file_type_regex'] = value
        self._print_set_message("File Type Regex", value)
        return self
    def set_file_type_exclude_regex(self, value):
        if not self._is_valid_regex(value):
            raise ValueError(f"{Fore.RED}Regex exclude file type must be a valid regular expression{Style.RESET_ALL}")
        self.config['file_type_exclude_regex'] = value
        self._print_set_message("File Type Exclude Regex", value)
        return self

    def set_file_name(self, value):
        if len(value) < 1:
            raise ValueError(f"{Fore.RED}File name must not be blank{Style.RESET_ALL}")
        self.config['file_name'] = value
        self._print_set_message("File Name", value)
        return self
    def set_file_names(self, values):
        for value in values:
            if len(value) < 1:
                raise ValueError(f"{Fore.RED}File name must not be blank{Style.RESET_ALL}")
        self.config['file_names'] = values
        self._print_set_message("File Names", values)
        return self
    def set_file_name_contains(self, value):
        if len(value) < 1:
            raise ValueError(f"{Fore.RED}File name contains must not be blank{Style.RESET_ALL}")
        self.config['file_name_contains'] = value
        self._print_set_message("File Name Contains", value)
        return self
    def set_file_name_starts_with(self, value):
        if len(value) < 1:
            raise ValueError(f"{Fore.RED}File name starts with must not be blank{Style.RESET_ALL}")
        self.config['file_name_starts_with'] = value
        self._print_set_message("File Name Starts With", value)
        return self
    def set_file_name_ends_with(self, value):
        if len(value) < 1:
            raise ValueError(f"{Fore.RED}File name ends with must not be blank{Style.RESET_ALL}")
        self.config['file_name_ends_with'] = value
        self._print_set_message("File Name Ends With", value)
        return self
    def set_file_name_regex(self, value):
        if not self._is_valid_regex(value):
            raise ValueError(f"{Fore.RED}Regex file name must be a valid regular expression{Style.RESET_ALL}")
        self.config['file_name_regex'] = value
        self._print_set_message("File Name Regex", value)
        return self
    def set_file_name_exclude_regex(self, value):
        if not self._is_valid_regex(value):
            raise ValueError(f"{Fore.RED}Regex exclude file name must be a valid regular expression{Style.RESET_ALL}")
        self.config['file_name_exclude_regex'] = value
        self._print_set_message("File Name Exclude Regex", value)
        return self

    def set_recursive(self, value):
        if not isinstance(value, bool):
            raise ValueError(f"{Fore.RED}Recursive must be a boolean value{Style.RESET_ALL}")
        self.config['recursive'] = value
        self._print_set_message("Recursive", value)
        return self
    def set_keep_source(self, value):
        if not isinstance(value, bool):
            raise ValueError(f"{Fore.RED}Keep Source must be a boolean value{Style.RESET_ALL}")
        self.config['keep_source'] = value
        self._print_set_message("Keep Source", value)
        return self

    def set_name(self, value):
        if not value or len(value) < 1:
            raise ValueError(f"{Fore.RED}Name must not be blank{Style.RESET_ALL}")
        self.config['name'] = value
        self._print_set_message("Name", value)
        return self
    def set_description(self, value):
        self.config['description'] = value
        self._print_set_message("Description", value)
        return self
    
    def _repeat_prompt_until_valid(self, prompt_func, input_condition=lambda x: True, invalid_message=None, *args):
        while True:
            try:
                result = prompt_func(*args)
                if input_condition(result):
                    return result
                else:
                    if invalid_message:
                        print(f"{Fore.RED}{invalid_message}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Invalid input{Style.RESET_ALL}")
            except ValueError as e:
                print(e)

    def _is_valid_regex(self, pattern):
        import re
        try:
            re.compile(pattern)
            return True
        except re.error:
            return False

    def _get_menu_text(self, prompt, options):
        menu = f"{prompt}{Style.RESET_ALL}\n"
        for key, value in options.items():
            menu += f" [{MENU_OPTION_VALUE_COLOR}{key}{Style.RESET_ALL}] {MENU_OPTION_NAME_COLOR}{value}{Style.RESET_ALL}\n"
        return menu

    def interactive_build(self):
        # ===== Source Directory =====
        
        def source_directory():
            option_map = {'0': False, '1': True}
            self.multiple_sources = option_map.get(self._repeat_prompt_until_valid(
                lambda: input(self._get_menu_text(f"Select your {Fore.CYAN}source directory mode{Style.RESET_ALL}:", {'0': 'Single Directory', '1': 'Multiple Directory'})).strip().lower(),
                input_condition=lambda x: x in ['0', '1'],
                invalid_message="Please enter a valid menu option"
            ))

            if self.multiple_sources:
                self.config['source_directories'] = []
                while True:
                    source = self._repeat_prompt_until_valid(
                        lambda: input(f"Enter {Fore.CYAN}source directory{Style.RESET_ALL} (or 'done' to finish): ").strip(),
                        input_condition=lambda x: x.lower() == 'done' or self._is_valid_path(x),
                        invalid_message="Please enter a valid absolute path or 'done'"
                    )
                    if source.lower() == 'done':
                        if not self.config['source_directories']:
                            print(f"{Fore.RED}At least one source directory must be specified{Style.RESET_ALL}")
                            continue
                        break
                    self.config['source_directories'].append(source)
                print(f"{Fore.GREEN}Added source directories:{Style.RESET_ALL}")
                for source in self.config['source_directories']:
                    print(f"{Fore.YELLOW}- {source}{Style.RESET_ALL}")
            else:
                self._repeat_prompt_until_valid(
                    lambda: input(f"Enter {Fore.CYAN}source directory{Style.RESET_ALL}: ").strip(),
                    input_condition=lambda x: self._try_set_option('source_directory', x),
                    invalid_message="Please enter a valid absolute path"
                )
        
        
        # ===== Destination Directory =====
        def destination_directory():
            
            menu_option = self._repeat_prompt_until_valid(
                lambda: input(self._get_menu_text(f"Select your {Fore.CYAN}destination directory mode{Style.RESET_ALL}:", {'0': 'Single Directory', '1': 'Multiple Directory'})).strip().lower(),
                input_condition=lambda x: x in ['0', '1'],
                invalid_message="Please enter a valid menu option"
            )
            self.multiple_destinations = menu_option == '1'
            if self.multiple_destinations:
                self.config['destination_directories'] = []
                while True:
                    destination = self._repeat_prompt_until_valid(
                        lambda: input(f"Enter {Fore.CYAN}destination directory{Style.RESET_ALL} (or 'done' to finish): ").strip(),
                        input_condition=lambda x: x.lower() == 'done' or self._is_valid_path(x),
                        invalid_message="Please enter a valid absolute path or 'done'"
                    )
                    if destination.lower() == 'done':
                        if not self.config['destination_directories']:
                            print(f"{Fore.RED}At least one destination directory must be specified{Style.RESET_ALL}")
                            continue
                        break
                    self.config['destination_directories'].append(destination)
                print(f"{Fore.GREEN}Added destination directories:{Style.RESET_ALL}")
                for destination in self.config['destination_directories']:
                    print(f"{Fore.YELLOW}- {destination}{Style.RESET_ALL}")
            else:
                self._repeat_prompt_until_valid(
                    lambda: input(f"Enter {Fore.CYAN}destination directory{Style.RESET_ALL}: ").strip(),
                    input_condition=lambda x: self._try_set_option('destination_directory', x),
                    invalid_message="Please enter a valid absolute path"
                )

        # ===== Filters =====
        def file_type_filter():
            menu_option = self._repeat_prompt_until_valid(
                lambda: input(self._get_menu_text(f"Which kind of {Fore.CYAN}file type filter{Style.RESET_ALL} would you like to configure?", {'0': 'Single File Type', '1': 'Multiple File Types', '2': 'Regex (include)', '3': 'Regex (exclude)', '4': 'Cancel (return to filter menu)'})).strip().lower(),
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
                        lambda: input(self._get_menu_text(f"{Fore.LIGHTRED_EX}You previously defined a {Fore.CYAN}Single File Type{Style.RESET_ALL}{Fore.LIGHTRED_EX} filter. Would you like to override it?{Style.RESET_ALL}", {'0': 'No (cancel)', '1': 'Yes'})).strip().lower(),
                        input_condition=lambda x: x in ['0', '1'],
                        invalid_message="Please enter a valid menu option"
                    )
                    if menu_option == '1':
                        continue_update = True
                    elif menu_option == '0':
                        continue_update = False
                if 'file_types' in self.config:
                    
                    menu_option = self._repeat_prompt_until_valid(
                        lambda: input(self._get_menu_text(f"{Fore.LIGHTRED_EX}You previously defined a {Fore.CYAN}Multiple File Type{Style.RESET_ALL}{Fore.LIGHTRED_EX} filter. How would you like to proceed?{Style.RESET_ALL}", {'0': 'Override it', '1': 'Add to it', '2': 'Cancel'})).strip().lower(),
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
                        lambda: input(f"Enter a {Fore.CYAN}file type{Style.RESET_ALL} (without the preceding '.'): ").strip().lower(),
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
                        lambda: input(self._get_menu_text(f"{Fore.LIGHTRED_EX}You previously defined a {Fore.CYAN}Multiple File Type Filter{Style.RESET_ALL}{Fore.LIGHTRED_EX}. How would you like to proceed?{Style.RESET_ALL}", {'0': 'Override it', '1': 'Add to it', '2': 'Cancel'})).strip().lower(),
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
                        lambda: input(self._get_menu_text(f"{Fore.LIGHTRED_EX}You previously defined a {Fore.CYAN}Single File Type Filter{Style.RESET_ALL}{Fore.LIGHTRED_EX}. How would you like to proceed?{Style.RESET_ALL}", {'0': 'Override it', '1': 'Add to it', '2': 'Cancel'})).strip().lower(),
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
                            lambda: input(f"Enter a {Fore.CYAN}file type{Style.RESET_ALL} (without the preceding '.') or 'done' to finish: ").strip().lower(),
                            input_condition=lambda x: x.isalnum(),
                            invalid_message="Please enter a valid file type (alphanumeric characters only, no spaces or dots)"
                        )
                        if file_type == 'done':
                            if not len(self.config['file_types']) > 0:
                                print(f"{Fore.RED}At least one file type must be specified{Style.RESET_ALL}")
                                continue
                            break
                        elif file_type in self.config['file_types']:
                            print(f"{Fore.YELLOW}{file_type}{Style.RESET_ALL} already included in {Fore.CYAN}file types{Style.RESET_ALL}")
                        else:
                            self.config['file_types'].append(file_type)
                    self._print_set_message("File Types", self.config['file_types'])
                    
            elif menu_option == '2':
                # Regex (include) File Type
                self._repeat_prompt_until_valid(
                    lambda: input(f"Enter a regular expression to match {Fore.CYAN}file type{Style.RESET_ALL}: ").strip().lower(),
                    input_condition=lambda x: self._try_set_option('file_type_regex', x),
                    invalid_message="The specified input is not a valid regular expression"
                )
            elif menu_option == '3':
                # Regex (exclude) File Type
                self._repeat_prompt_until_valid(
                    lambda: input(f"Enter a regular expression to exclude {Fore.CYAN}file type{Style.RESET_ALL}: ").strip().lower(),
                    input_condition=lambda x: self._try_set_option('file_type_exclude_regex', x),
                    invalid_message="The specified input is not a valid regular expression"
                )
            elif menu_option == '4':
                return
        def file_name_filter():
            
            menu_option = self._repeat_prompt_until_valid(
                lambda: input(self._get_menu_text(f"Which kind of {Fore.CYAN}file name filter{Style.RESET_ALL} would you like to configure?", {'0': 'Single Exact Name', '1': 'Multiple Exact Names', '2': 'Contains', '3': 'Starts With', '4': 'Ends With', '5': 'Regex (include)', '6': 'Regex (exclude)', '7': 'Cancel (return to filter menu)'})).strip().lower(),
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
                        lambda: input(self._get_menu_text(f"{Fore.LIGHTRED_EX}You previously defined a {Fore.CYAN}Single File Name{Style.RESET_ALL}{Fore.LIGHTRED_EX} filter. Would you like to override it?{Style.RESET_ALL}", {'0': 'No (cancel)', '1': 'Yes'})).strip().lower(),
                        input_condition=lambda x: x in ['0', '1'],
                        invalid_message="Please enter a valid menu option"
                    )
                    if menu_option == '1':
                        continue_update = True
                    elif menu_option == '0':
                        continue_update = False
                if 'file_names' in self.config:
                    
                    menu_option = self._repeat_prompt_until_valid(
                        lambda: input(self._get_menu_text(f"{Fore.LIGHTRED_EX}You previously defined a {Fore.CYAN}Multiple File Name{Style.RESET_ALL}{Fore.LIGHTRED_EX} filter. How would you like to proceed?{Style.RESET_ALL}", {'0': 'Override it', '1': 'Add to it', '2': 'Cancel'})).strip().lower(),
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
                        lambda: input(f"Enter a {Fore.CYAN}file name{Style.RESET_ALL} {Fore.BLACK}(note: do not include a file type extension - it will not be matched by this filter){Style.RESET_ALL}: ").strip().lower(),
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
                        lambda: input(self._get_menu_text(f"{Fore.LIGHTRED_EX}You previously defined a {Fore.CYAN}Multiple File Name{Style.RESET_ALL}{Fore.LIGHTRED_EX} filter. How would you like to proceed?{Style.RESET_ALL}", {'0': 'Override it', '1': 'Add to it', '2': 'Cancel'})).strip().lower(),
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
                        lambda: input(self._get_menu_text(f"{Fore.LIGHTRED_EX}You previously defined a {Fore.CYAN}Single File Name{Style.RESET_ALL}{Fore.LIGHTRED_EX} filter. How would you like to proceed?{Style.RESET_ALL}", {'0': 'Override it', '1': 'Add to it', '2': 'Cancel'})).strip().lower(),
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
                            lambda: input(f"Enter a {Fore.CYAN}file name{Style.RESET_ALL} (without the file type extension) or 'done' to finish: ").strip().lower(),
                            input_condition=lambda x: len(x) > 0,
                            invalid_message="Please enter a valid file name"
                        )
                        if file_name == 'done':
                            if not len(self.config['file_names']) > 0:
                                print(f"{Fore.RED}At least one file name must be specified{Style.RESET_ALL}")
                                continue
                            break
                        elif file_name in self.config['file_names']:
                            print(f"{Fore.YELLOW}{file_name}{Style.RESET_ALL} already included in {Fore.CYAN}file names{Style.RESET_ALL}")
                        else:
                            self.config['file_names'].append(file_name)
                    self._print_set_message("File Names", self.config['file_names'])
                    
            elif menu_option == '2':
                # Contains
                self._repeat_prompt_until_valid(
                    lambda: input(f"Enter a substring to match within a {Fore.CYAN}file name{Style.RESET_ALL} (without the file type extension): ").strip().lower(),
                    input_condition=lambda x: self._try_set_option('file_name_contains', x),
                    invalid_message="Please enter a valid file name substring"
                )
            elif menu_option == '3':
                # Starts With
                self._repeat_prompt_until_valid(
                    lambda: input(f"Enter a substring to match the start of a {Fore.CYAN}file name{Style.RESET_ALL}: ").strip().lower(),
                    input_condition=lambda x: self._try_set_option('file_name_starts_with', x),
                    invalid_message="Please enter a valid file name substring"
                )
            elif menu_option == '4':
                # Ends With
                self._repeat_prompt_until_valid(
                    lambda: input(f"Enter a substring to match the end of a {Fore.CYAN}file name{Style.RESET_ALL} (without the file type extension): ").strip().lower(),
                    input_condition=lambda x: self._try_set_option('file_name_ends_with', x),
                    invalid_message="Please enter a valid file name substring"
                )
            elif menu_option == '5':
                # Regex (include)
                self._repeat_prompt_until_valid(
                    lambda: input(f"Enter a regex pattern to match files by {Fore.CYAN}file name{Style.RESET_ALL}: ").strip().lower(),
                    input_condition=lambda x: self._try_set_option('file_name_regex', x),
                    invalid_message="The specified input is not a valid regular expression"
                )
                
            elif menu_option == '6':
                # Regex (exclude)
                self._repeat_prompt_until_valid(
                    lambda: input(f"Enter a regex pattern to exclude files by {Fore.CYAN}file name{Style.RESET_ALL}: ").strip().lower(),
                    input_condition=lambda x: self._try_set_option('file_name_exclude_regex', x),
                    invalid_message="The specified input is not a valid regular expression"
                )
            elif menu_option == '7':
                return
        def filters():
            has_file_type_filter = False
            has_name_filter = False
            while True:
                menu_option = self._repeat_prompt_until_valid(
                    lambda: input(self._get_menu_text(f"Select a {Fore.CYAN}file filter mode{Style.RESET_ALL} to configure (you will have the chance to define multiple):", {'0': 'File Type', '1': 'File Name', '2': 'Done / Apply All Filters'})).strip().lower(),
                    input_condition=lambda x: x in ['0', '1', '2'],
                    invalid_message="Please enter a valid menu option"
                )
                if menu_option == '0':
                    file_type_filter()
                    has_file_type_filter = True
                elif menu_option == '1':
                    file_name_filter()
                    has_name_filter = True
                elif menu_option == '2':
                    if not has_file_type_filter and not has_name_filter:
                        
                        menu_option = self._repeat_prompt_until_valid(
                            lambda: input(self._get_menu_text(f"{Fore.RED}Neither a file type nor file name filter has been defined. This will match ALL files in the source directory. Is this correct?{Style.RESET_ALL}", {'0': 'No', '1': 'Yes'})).strip().lower(),
                            input_condition=lambda x: x in ['0', '1'],
                            invalid_message="Please enter a valid menu option"
                        )
                        if menu_option == '1':
                            return
                        else:
                            continue
                    return

        # ===== Keep Source =====
        def keep_source():
            option_map = {'0': False, '1': True}
            
            self._repeat_prompt_until_valid(
                lambda: input(self._get_menu_text(f"After the file move(s) are done, do you want to keep the source file or remove it?", {'0': 'Keep Source', '1': 'Remove Source'})).strip().lower(),
                input_condition=lambda x: self._try_set_option('keep_source', option_map.get(x)),
                invalid_message="Please enter a valid menu option"
            )

        # ===== Recursive =====
        def recursive():
            option_map = {'0': False, '1': True}
            
            self._repeat_prompt_until_valid(
                lambda: input(self._get_menu_text(f"Should file matching be recursive (i.e., traverse any subdirectories in the source directory to find matches)?", {'0': 'No', '1': 'Yes'})).strip().lower(),
                input_condition=lambda x: self._try_set_option('recursive', option_map.get(x)),
                invalid_message="Please enter a valid menu option"
            )

        # ===== Name =====
        def name():
            self._repeat_prompt_until_valid(
                lambda: input(f"Enter a name for your file mover (a short identifier): ").strip().lower(),
                input_condition=lambda x: self._try_set_option('name', x),
                invalid_message="Please enter a valid string"
            )

        # ===== Description =====
        def description():
            self._repeat_prompt_until_valid(
                lambda: input(f"Enter a description for your file mover (optional): ").strip().lower(),
                input_condition=lambda x: self._try_set_option('description', x)
            )
        
        # ===== Rename Configuration =====
        def timestamp_config():
            
            menu_option = self._repeat_prompt_until_valid(
                lambda: input(self._get_menu_text(f"Should a {Fore.CYAN}timestamp{Style.RESET_ALL} be added to moved files?", {'0': 'No', '1': 'Yes'})).strip().lower(),
                input_condition=lambda x: x in ['0', '1'],
                invalid_message="Please enter a valid menu option"
            )
            if menu_option == '0':
                return
            self._repeat_prompt_until_valid(
                lambda: input(f"(Optional) Enter the {Fore.CYAN}timestamp format{Style.RESET_ALL} (leave blank for default): ").strip().lower(),
                input_condition=lambda x: self._try_set_timestamp_option('format', x),
                invalid_message=None
            )
            self._repeat_prompt_until_valid(
                lambda: input(f"(Optional) Enter the {Fore.CYAN}timestamp timezone{Style.RESET_ALL} (leave blank for default): ").strip().lower(),
                input_condition=lambda x: self._try_set_timestamp_option('timezone', x),
                invalid_message=None
            )
            
            option_map = {'0': TimestampPosition.START.value, '1': TimestampPosition.AFTER_PREFIX.value, '2': TimestampPosition.BEFORE_SUFFIX.value, '3': TimestampPosition.END.value}
            
            menu_option = self._repeat_prompt_until_valid(
                lambda: input(self._get_menu_text(f"Select the {Fore.CYAN}position{Style.RESET_ALL} the timestamp should be placed:", {'0': 'Start', '1': 'After Prefix', '2': 'Before Suffix', '3': 'End'})).strip().lower(),
                input_condition=lambda x: self._try_set_timestamp_option('position', option_map.get(x)),
                invalid_message=None
            )
            
            
        def rename_config():
            
            menu_option = self._repeat_prompt_until_valid(
                lambda: input(self._get_menu_text(f"Would you like to configure {Fore.CYAN}renaming files{Style.RESET_ALL} when they're moved?", {'0': 'No', '1': 'Yes'})).strip().lower(),
                input_condition=lambda x: x in ['0', '1'],
                invalid_message="Please enter a valid menu option"
            )
            if menu_option == '0':
                return
            
            # Case sensitive
            
            menu_option = self._repeat_prompt_until_valid(
                lambda: input(self._get_menu_text(f"Should rename replace matching rules be {Fore.CYAN}case sensitive{Style.RESET_ALL}?", {'0': 'No', '1': 'Yes'})).strip().lower(),
                input_condition=lambda x: x in ['0', '1'],
                invalid_message="Please enter a valid menu option"
            )
            if menu_option == '1':
                self.set_rename_case_sensitive(True)
            elif menu_option == '0':
                self.set_rename_case_sensitive(False)
            
            # Prefix
            self._repeat_prompt_until_valid(
                lambda: input(f"(Optional) Enter a {Fore.CYAN}prefix{Style.RESET_ALL} to match files to rename: ").strip().lower(),
                input_condition=lambda x: self._try_set_rename_option('prefix', x),
                invalid_message=None
            )
            # Suffix
            self._repeat_prompt_until_valid(
                lambda: input(f"(Optional) Enter a {Fore.CYAN}suffix{Style.RESET_ALL} to match files to rename: ").strip().lower(),
                input_condition=lambda x: self._try_set_rename_option('suffix', x),
                invalid_message=None
            )

            while True:
                menu_option = self._repeat_prompt_until_valid(
                    lambda: input(self._get_menu_text(f"Add a {Fore.CYAN}text replace rule{Style.RESET_ALL}? You may define 0 or more", {'0': 'Add Rule', '1': 'Done'})).strip().lower(),
                    input_condition=lambda x: x in ['0', '1'],
                    invalid_message="Please enter a valid menu option"
                )
                if menu_option == '1':
                    break
                search = self._repeat_prompt_until_valid(
                    lambda: input(f"Enter the text to {Fore.CYAN}search/match{Style.RESET_ALL}: ").strip().lower(),
                    input_condition=lambda x: len(x) > 0,
                    invalid_message="Search cannot be blank"
                )
                replace = self._repeat_prompt_until_valid(
                    lambda: input(f"Enter the text to {Fore.CYAN}replace{Style.RESET_ALL} the matched text in search with: ").strip().lower()
                )
                try:
                    self.add_replace_rule({"search": search, "replace": replace})
                except ValueError as e:
                    print(e)
            
            timestamp_config()

        source_directory()
        destination_directory()

        filters()
        
        rename_config()
        keep_source()
        recursive()

        name()
        description()
        return self.config
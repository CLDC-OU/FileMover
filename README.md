# File Mover

it mova da files :3

## Features

- [x] Move files from one location to another
- [x] Define custom "Movers" that specify file movement rules & patterns
- [x] Filter files by Name
    - [x] exact name or list of names
    - [x] name based on regex rules
    - [x] file name starts with or ends with a specific string
    - [x] file name contains a specific string
- [x] Filter files by Extension
    - [x] exact extension or list of extensions
    - [x] extension based on regex rules
- [ ] Filter files by other attributes
    - [ ] date (created, modified)
    - [ ] file size
- [x] Rename files when moving from one location to another
    - [x] Timestamp files with customizable formats and positions
    - [x] Add prefixes and suffixes to moved files
    - [x] Search and replace text in moved file names
- [x] Move files to a single or multiple directories
- [x] Copy files instead of moving (you're telling me the file mover can do more than moving???)
- [ ] Support environment variables like %HOMEPATH%
- [ ] Support relative file paths
- [ ] Custom scheduling to run at specific dates/times or frequencies
- [ ] Delete files instead of moving them (why would you do that???)



## Setup / Use

### From the Command Line

1. Install the package. Replace `<VERSION>` with the desired version number (e.g., `1.0.0`):
    ```bash
    pip install filemover @ git+https://github.com/CLDC-OU/FileMover.git@<VERSION>
    ```
2. Run the desired [command](#commands) from the command line

#### Commands


| Command | Options | Description |
|-----|-----|-----|
| `build-mover` | None | Starts an interactive script that walks you through configuring a new File Mover. This script is not necessary for running a File Mover, but makes setup extremely easy |
| `run-mover` | `j` (`--json_file`), `y` (`--yaml_file`) | Specify the path to a JSON or YAML file with the configuration for a File Mover and run it |

#### Examples

```bash
build-mover
```

```bash
run-mover --json-file=C:/User/Documents/example_mover.json
```

```bash
run-mover -y "C:/User/Documents/Folder with a space/example_mover.yaml"
```

```bash
run-mover -j ./mover.json
```

### Within a Python project

1. Import the package into your Python project. Replace `<VERSION>` with the desired version number (e.g., `1.0.0`):
    ```bash
    pip install filemover @ git+https://github.com/CLDC-OU/FileMover.git@<VERSION>
    ```
2. Create and configure a [Mover](#mover%20configuration)
3. Use the Mover in your Python code:
    ```python
    import json
    from filemover import Mover

    # Load your config
    with open("path/to/mover/config.json", 'r') as file:
        config = json.load(file)

    # Create a mover
    mover = Mover(**config)

    # Run the mover
    mover.move_files()
    ```

## Mover Configuration

There are 2 options for creating a custom Mover. Well... technically there is 1 option... the other "option" is just a script to make it significantly easier / more intuitive.

Mover's are configured with a dictionary - which you can read from a file or just use directly in python.

The [command line script](#commands) supports loading from json or yaml formats, but you can use any format in your own application if you import the package.

You can find some examples of configuration files in the `examples/` directory

### Interactive Mover Builder Script

After installing the `filemover` package, you can use the `build-mover` command directly from the command line. This will start up an interactive step-by-step process that walks you through every configuration option and allows you to save the final configuration to a file or print it out. See [Commands](#commands)

### General Configuration

> [!NOTE] 
> You must specify one of `destination_directory` or `destination_directories` and one of `source_directory` or `source_directories`. If all you wanna do is mova tha files (a true file mover), that's all you need to configure
> 
> If you wanna do fancy stuff like only move certain files or... god forbid... COPY files D: well, heh, we've got that too for the low, low price of configuration

| Option | Type | Description |
|-----|-----|-----|
| `mover_name` | `string` | A name for the mover. This will print in logs |
| `mover_description`? | `string` | A more detailed description for the mover. This can be used for whatever notes to identify the mover later. It does not change any behavior within the application. It may be included in reports in the future |
| `source_directory`* | `string` | A single source directory to move files from. Relative path structures, network locations, and path variables (e.g., `%HOMEPATH%`) are all supported. |
| `source_directories`* | `list` or `string` | A list of directories to move files from. If `source_directory` is set, this property will be ignored. |
| `destination_directory`* | `string` | A single destination directory to move files to. Relative path structures, network locations, and path variables (e.g., `%HOMEPATH%`) are all supported |
| `destination_directories`* | `list` of `string` | A list of directories to move files to. Moved files will be attempted to be placed in each of these (all conditions are applied together as one). If `destination_directory` is set, this property will be ignored. |
| `keep_source_behavior`? | What should be done with the source files (not restricted to moving!) | Default `"never_keep_source"`. See [Keep Source Behavior](#keep-source-behavior) |
| `recursive`? | Whether to recursively search subdirectory | Default: `false`. If `true` will traverse subdirectories within the source directory and match files. Destination files will always be placed directly in the `source_directory` |
| `destination_collision_behavior`? | How collisions in the destination should be handled | Default: `"ignore"`. See [Destination Collision Behavior](#destination-collision-behavior) |
| `collision_avoidance_behavior`? | How collisions should be avoided by the mover | Default: `"none"` See [Collision Avoidance Behavior](#collision-avoidance-behavior) |
| `match_files`? | The configuration used to match files | See [File Matching](#file-matching). If omitted, all files in the source are processed |
| `rename`? | The configuration used to rename files that are moved | See [File Renaming](#file-renaming) |



### Keep Source Behavior

This option determines what to do with the source file when they're processed (holy moly this thing can do more than moving :O).

| Option | Description |
|-----|-----|
| `"never_keep_source"` | Delete the source file (i.e., 'move' the file) |
| `"keep_source"` | Keep the source file (i.e., 'copy' the file) |
| `"keep_source_if_any_collide"` | Keep the source file if ANY destination files collide (delete otherwise) |
| `"keep_source_if_all_collide"` | Keep the source file if ALL destination files collide (delete otherwise) |
| `"keep_source_if_none_collide"` | Keep the source file if NO destination files collide (i.e., delete if any collide) |

### Destination Collision Behavior

This option determines how file collisions (i.e., a file from the source location colliding with an existing file in the destination location) are handled. This behavior is applied on each collision, so in theory if you have the Mover rename each file with the exact same name, it could be replacing the same file on every move.

| Option | Description |
|-----|-----|
| `"ignore"` | Ignore/skip the file move operation (do nothing) and proceed |
| `"overwrite"` | Overwrite the existing file |

### Collision Avoidance Behavior

Note: The move operation being canceled means **no files will be moved**. This is a check done before starting to process any files. For behavior during the file move see [Destination Collision Behavior](#destination-collision-behavior).

| Option | Description | Note |
|-----|-----|-----|
| `"none"` | Continue with the move operation | Collisions will not be avoided (i.e., no pre-check is done) |
| `"cancel_move_if_any_collide"` | Cancel the move operation if any files would collide | The entire move operation will be canceled if it will result in any (1 or more) file collisions |
| `"cancel_move_if_all_collide"` | Cancel the move operation if all files would collide | The entire move operation will be canceled if it will result in every moved file colliding. If the number of collisions is any amount less than the total matched files, the move proceeds |

### File Matching

The `match_files` property in the config defines what and how files will be matched by the Mover.

Each file match rule has the following properties:

| Property | Type | Description |
|-----|-----|-----|
| `enabled` | boolean | Whether to match files. This should always be true |
| `operator` | [File Match Rule Operator](#file-match-rule-operator) | The condition that file match rules are applied on |
| `rules` | `list` of [File Match Rule](#file-match-rule) | The rules to match files with |

### File Match Rule Operator

This operator applies to all rules. There is currently no way to define nested operations. For this, just use multiple Movers. For "not" matches, use regex exclude modes.

| Option | Description |
|-----|-----|
| `"and"` | AND (the conditions of all rules are satisfied) |
| `"or"` | OR (the conditions of at least one of the rules are satisfied) |

### File Match Rule

| Property | Type | Description |
|-----|-----|-----|
| `type` | [File Match Type](#file-match-types) | The part/property of the file this rule applies to |
| `mode` | [File Type Match Mode](#file-type-match-mode) or [File Name Match Mode](#file-name-match-mode) | The type of matching this rule does |
| `value` | `string`, `list`, or `regex` depending on the value of the `mode` property | The value to match with the rule |
| `case_sensitive`? | `boolean` | Only supported with file name matches (file type matching is always case insensitive) |

#### File Match Types

Applies to property `type` of [File Match Rule](#file-match-rule)

| Type | Description |
|-----|-----|
| `"file_type"` | Match file types/extensions |
| `"file_name"` | Match file names |

#### File Type Match Mode

Applies to property `mode` of [File Match Rule](#file-match-rule) for the `"file_type"` [File Match Type](#file-match-types)

| Type | Description |
|-----|-----|
| `"single_exact"` | Match file types with a single extension |
| `"multiple_exact"` | Match file types among a list of extensions |
| `"regex_include"` | Match file types using a regular expression |
| `"regex_exclude"` | Match file types that aren't matched by a regular expression |

#### File Name Match Mode

Applies to property `mode` of [File Match Rule](#file-match-rule) for the `"file_name"` [File Match Type](#file-match-types)

| Type | Description |
|-----|-----|
| `"single_exact"` | Match files with a single exact name |
| `"multiple_exact"` | Match files among a list of exact names |
| `"contains"` | Match files with a name containing a specific substring |
| `"starts_with"` | Match files with a name that starts with a specific substring |
| `"ends_with"` | Match files with a name that ends with a specific substring |
| `"regex_include"` | Match files with a name that matches a regular expression |
| `"regex_exclude"` | Match files that have a name that doesn't match a regular expression |

### File Renaming

| Property | Type | Description |
|-----|-----|-----|
| `enabled` | `boolean` | Default `false`. Whether to apply renaming to moved files |
| `replace` | `list` of [Rename Rules](#rename-rule) | Basic string match replacements to apply to the names of moved files |
| `case_sensitive` | `boolean` | Default: `false`. Whether the rename rule searches are case sensitive |
| `prefix`? | `string` | A fixed prefix to add to moved files |
| `suffix`? | `string` | A fixed suffix to add to moved files |
| `add_timestamp` | [Add Timestamp Config](#add-timestamp) | Configuration to add a timestamp to the name of the moved file |

#### Rename Rule

#### Add Timestamp

| Property | Type | Description |
|-----|-----|-----|
| `enabled` | `boolean` | Whether to add the timestamp |
| `format`? | `string` | Default: `"%Y-%m-%d_%H-%M-%S"`. A valid `strftime()` timestamp format. |
| `timezone`? | `string` | Default: local timezone. Must be a valid IANA timezone identifier (https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) |
| `position`? | [Timestamp Position](#timestamp-position) | Default: `"after_prefix"` |

#### Timestamp Position

| Type | Description |
|-----|-----|
| `"start"` | Add the timestamp to the very beginning of the file name (timestamp + prefix + name + suffix) |
| `"after_prefix"` | Add the timestamp at the beginning of the file name after the prefix (prefix + timestamp + name + suffix) |
| `"before_suffix"` | Add the timestamp to the end of the file name before the suffix (prefix + name + timestamp + suffix) |
| `"end"` | Add the timestamp to the very end of the file name (prefix + name + suffix + timestamp) |

## Development Setup

This section is for developers who want to contribute to the project or run it locally without importing it as a package.

1. Set up a virtual environment (recommended)
    ```bash
    python -m venv .venv
    ```
2. Activate the virtual environment
    - Windows:
        ```bash
        .venv\Scripts\activate
        ```
3. Install the required packages
    ```bash
    pip install -r requirements.txt
    ```
4. Install the package
    ```bash
    pip install .
    ```

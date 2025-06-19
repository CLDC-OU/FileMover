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
- [ ] File size filtering
- [ ] Delete files instead of moving them (why would you do that???)



## Setup / Use

1. Import the package into your Python project. Replace `<VERSION>` with the desired version number (e.g., `1.0.0`):
    ```bash
    pip install file_mover @ git+https://github.com/CLDC-OU/FileMover.git@<VERSION>
    ```
2. Create and configure a [Mover](#mover%20configuration)
3. Use the Mover in your Python code:
    ```python
    import json
    from file_mover import Mover

    # Load your config
    with open("path/to/mover/config.json", 'r') as file:
        config = json.load(file)

    # Create a mover
    mover = Mover(**config)

    # Run the mover
    mover.move_files()
    ```


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

## Mover Configuration

There are 2 options for creating a custom Mover.

### Interactive Mover Builder Script



### Direct JSON Setup

#### Rules
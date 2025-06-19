# File Mover

it mova da files :3

## Features

- [x] Move files from one location to another
- [x] Define custom "Movers" that specify file movement rules & patterns
    - [x] Filter files by name based on regex rules
    - [x] Filter files by file extension
    - [ ] Filter files by a list of rules
- [x] Rename files when moving from one location to another
- [x] Copy files instead of moving (you're telling me the file mover can do more than moving???)
- [ ] Support environment variables like %HOMEPATH%
- [ ] Support relative file paths
- [ ] Custom scheduling to run at specific dates/times or frequencies


## Setup

1. Ensure all [Dependencies](#dependencies) have been installed
2. Create and configure a [Mover](#mover%20configuration)
3. (Optional) Set up additional configuration


## Dependencies

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
from filemover.mover import Mover
from filemover.mover_builder import InteractiveMoverConfigBuilder
from colorama import Fore, Style
import argparse
import json
import yaml

def run_mover():
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--json_config", help="Specify a path to a JSON configuration file")
    parser.add_argument("-y", "--yaml_config", help="Specify a path to a YAML configuration file")

    args = parser.parse_args()
    config = None
    
    if args.json_config and args.yaml_config:
        print(f"{Fore.RED}Only one of {Fore.LIGHTBLACK_EX}--json_config{Fore.RED} and {Fore.LIGHTBLACK_EX}--yaml_config{Fore.RED} may be specified{Style.RESET_ALL}")
        return

    if args.json_config:
        try:
            with open(args.json_config, "r") as f:
                config = json.load(f)
                if not config:
                    raise FileNotFoundError("Failed to load config from the provided json file")
                print(f"{Fore.GREEN}Loaded config from JSON file{Style.RESET_ALL}")
        except BaseException as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
            return

    if args.yaml_config:
        try:
            with open(args.yaml_config, "r") as f:
                config = yaml.safe_load(f)
                if not config:
                    raise FileNotFoundError("Failed to load config from the provided yaml file")
                print(f"{Fore.GREEN}Loaded config from YAML file{Style.RESET_ALL}")
        except BaseException as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
            return

    if not config is None and isinstance(config, dict):
        mover = Mover(**config)
        mover.move_files()
    else:
        print(f"{Fore.RED}Config must be provided with either the {Fore.LIGHTBLACK_EX}--json_config{Fore.RED} or {Fore.LIGHTBLACK_EX}--yaml_config{Fore.RED} options{Style.RESET_ALL}")

def build_mover():
    print(f"{Fore.GREEN}Starting Interactive File Mover Configuration Builder...{Style.RESET_ALL}")
    builder = InteractiveMoverConfigBuilder()
    builder.interactive_build()

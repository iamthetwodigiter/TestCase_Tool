import os
import sys
import argparse
from pathlib import Path
from colorama import init, Fore, Style
from genetate_testcases import generate_testcases
from validate_testcases import validate_testcases
import pyfiglet

init()

def print_header(text):
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}💠 {text}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")


def print_error(text):
    print(f"{Fore.RED}❌ {text}{Style.RESET_ALL}")

def print_info(text):
    print(f"{Fore.YELLOW}ℹ️ {text}{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(
        description="Test Case Generator and Validator Tool by thetwodigiter",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "action",
        choices=["generate", "validate", "both"],
        help="Action to perform (generate/validate/both)",
    )

    parser.add_argument(
        "--max-cases",
        type=int,
        default=100,
        help="Maximum number of test cases per file (default: 100)",
    )

    parser.add_argument(
        "--num-files",
        type=int,
        default=10,
        help="Number of test files to generate (default: 10)",
    )

    args = parser.parse_args()

    working_dir = os.getcwd()

    try:
        app = pyfiglet.figlet_format('TestCase Tool',font='doom')
        print(Fore.MAGENTA + app)
        dev = pyfiglet.figlet_format('by  thetwodigiter',font='doom')
        print(Fore.BLUE + dev)
        print_info(f"Working directory: {working_dir}")

        if args.action in ["generate", "both"]:
            print_header("Starting Test Case Generation")
            generation_success = generate_testcases(args.max_cases, args.num_files)

            
            if not generation_success and args.action == "both":
                print_error("Test case generation failed. Skipping validation.")
                sys.exit(1)

        if args.action in ["validate", "both"]:
            
            if args.action == "validate" or (
                args.action == "both" and generation_success
            ):
                print_header("Starting Test Case Validation")
                validate_testcases(args.max_cases, args.num_files)

    except Exception as e:
        print_error(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
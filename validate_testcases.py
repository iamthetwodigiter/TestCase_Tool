import os
import sys
from io import StringIO
from pathlib import Path
from colorama import init, Fore, Style

init()

def print_header(text):
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}💠 {text}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")

def print_error(text):
    print(f"{Fore.RED}❌ {text}{Style.RESET_ALL}")

def print_success(text):
    print(f"{Fore.GREEN}✅ {text}{Style.RESET_ALL}")

def print_info(text):
    print(f"{Fore.BLUE}ℹ️  {text}{Style.RESET_ALL}")

def check_language_support(ext):
    """Check if the required language support is available"""
    try:
        if ext == "py":
            import sys

            return True, f"Python {sys.version.split()[0]} found"
        elif ext == "java":
            output = os.popen("java -version 2>&1").read()
            if "java version" in output.lower() or "openjdk version" in output.lower():
                return True, f"Java {output.split()[2].strip('\"')} found"
            return False, "Java Runtime not found"
        elif ext in ["cpp", "c"]:
            if ext == "cpp":
                output = os.popen("g++ --version 2>&1").read()
                if not "not" in output.lower():
                    return True, f"G++ {output.split()[3]} found"
                return False, "G++ compiler not found"
            else:
                output = os.popen("gcc --version 2>&1").read()
                if not "not" in output.lower():
                    return True, f"GCC {output.split()[3]} found"
                return False, "GCC compiler not found"
        return False, f"Unknown language extension: {ext}"
    except Exception as e:
        return False, str(e)

def select_solution():
    """Let user select a solution file to validate against"""
    solutions = {
        "py": "solution.py",
        "java": "Solution.java",
        "c": "solution.c",
        "cpp": "solution.cpp",
    }

    available_solutions = []
    for ext, filename in solutions.items():
        if os.path.exists(filename):

            supported, message = check_language_support(ext)
            if supported:
                available_solutions.append((ext, filename))
                print_success(f"Found {filename} ({message})")
            else:
                print_error(f"Found {filename} but {message}")

    if not available_solutions:
        print_error("No usable solution files found!")
        print_info("Please ensure you have the required language support installed:")
        print_info("- Python: Required for .py files")
        print_info("- Java JDK: Required for .java files")
        print_info("- GCC: Required for .c files")
        print_info("- G++: Required for .cpp files")
        return None, None

    print(f"\n{Fore.BLUE}Available Solution Files{Style.RESET_ALL}")
    for idx, (ext, filename) in enumerate(available_solutions, 1):
        print(f"{Fore.BLUE}{idx}. {filename}{Style.RESET_ALL}")

    while True:
        try:
            choice = int(
                input(
                    f"\n{Fore.GREEN}Select a solution file (1-{len(available_solutions)}): {Style.RESET_ALL}"
                )
            )
            if 1 <= choice <= len(available_solutions):
                return available_solutions[choice - 1]
        except ValueError:
            pass
        print_error("Invalid choice! Please try again.")

def capture_output(input_data, solution_file, ext):
    """Run the solution file with given input and return output"""

    with open("temp_input.txt", "w") as f:
        f.write(input_data)

    if ext == "py":
        output = os.popen(f"python {solution_file} < temp_input.txt").read()
    elif ext == "java":
        os.system(f"javac {solution_file}")
        class_name = solution_file.split(".")[0]
        output = os.popen(f"java {class_name} < temp_input.txt").read()
    elif ext == "cpp":
        os.system(f"g++ {solution_file} -o solution")
        output = os.popen(f"solution.exe < temp_input.txt").read()
    elif ext == "c":
        os.system(f"gcc {solution_file} -o solution")
        output = os.popen(f"solution.exe < temp_input.txt").read()

    os.remove("temp_input.txt")
    if ext in ["cpp", "c"]:
        os.remove("solution.exe")
    elif ext == "java":
        os.remove(f"{solution_file.split('.')[0]}.class")

    return output.strip()

def validate_testcases(max_cases=None, num_files=None):
    print_header("Test Case Validation")

    try:
        ext, solution_file = select_solution()
        if not solution_file:
            print_error("No valid solution file available for validation")
            return False

        print_success(f"Selected solution: {solution_file}")

        testcase_dir = Path(".")
        input_files = sorted([f for f in testcase_dir.glob("in*.txt")])

        if not input_files:
            print_error("No test cases found to validate!")
            return False

        all_valid = True
        total_tests = len(input_files)
        passed_tests = 0

        print_header("Test Case Validation Started")

        for input_file in input_files:
            output_file = testcase_dir / f"out{input_file.name[2:]}"

            if not output_file.exists():
                print_error(f"Missing output file for {input_file.name}")
                all_valid = False
                continue

            try:

                with open(input_file, "r") as f:
                    input_data = f.read()
                with open(output_file, "r") as f:
                    expected_output = f.read().strip()

                actual_output = capture_output(input_data, solution_file, ext)

                if actual_output != expected_output:
                    print_error(f"Test case failed: {input_file.name}")
                    print_info("Expected output:")
                    print(f"{Fore.WHITE}{expected_output}{Style.RESET_ALL}")
                    print_info("Actual output:")
                    print(f"{Fore.WHITE}{actual_output}{Style.RESET_ALL}")
                    all_valid = False
                else:
                    passed_tests += 1
                    print_success(f"Test case passed: {input_file.name}")

            except Exception as e:
                print_error(f"Error validating {input_file.name}: {str(e)}")
                all_valid = False

        print_header("Test Results Summary")
        print_info(f"Total test cases: {total_tests}")
        print_info(f"Passed: {passed_tests}")
        print_info(f"Failed: {total_tests - passed_tests}")

        if all_valid:
            print(
                f"\n{Fore.GREEN}🎉 All test cases passed successfully! 🎉{Style.RESET_ALL}"
            )
            return True
        else:
            print_error("Some test cases failed. Please check the output above.")
            return False

    except Exception as e:
        print_error(f"Validation failed: {str(e)}")
        return False

if __name__ == "__main__":

    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    validate_testcases()
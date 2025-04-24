import os
import sys
import random
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
    print(f"{Fore.YELLOW}ℹ️ {text}{Style.RESET_ALL}")

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
                if output and not "not" in output.lower():
                    return True, f"G++ {output.split()[3]} found"
                return False, "G++ compiler not found"
            else:
                output = os.popen("gcc --version 2>&1").read()
                if output and not "not" in output.lower():
                    return True, f"GCC {output.split()[3]} found"
                return False, "GCC compiler not found"
        return False, f"Unknown language extension: {ext}"
    except Exception as e:
        return False, str(e)

def select_solution():
    """Let user select a base solution file"""
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
        sys.exit(1)

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
                return available_solutions[choice - 1][1]
        except ValueError:
            pass
        print_error("Invalid choice! Please try again.")

def get_test_params():
    """Get test generation parameters from user"""
    while True:
        try:
            max_t = input(
                f"\n{Fore.GREEN}Enter maximum number of test cases per file [default: 100]: {Style.RESET_ALL}"
            )
            max_t = int(max_t) if max_t.strip() else 100

            if max_t < 1:
                print_error("Number must be positive!")
                continue

            num_files = input(
                f"{Fore.GREEN}Enter number of test files to generate [default: 10]: {Style.RESET_ALL}"
            )
            num_files = int(num_files) if num_files.strip() else 10

            if num_files < 1:
                print_error("Number must be positive!")
                continue

            return max_t, num_files

        except ValueError:
            print_error("Please enter valid numbers!")

def generate_test_case(solution_file, max_t):
    """Generate test cases and get output from solution file"""
    input_str = ""

    t = random.randint(1, max_t)
    input_str += str(t) + "\n"

    while t > 0:
        x = random.randint(1, 10)
        y = random.randint(1, 10)
        input_str += f"{x} {y}\n"
        t -= 1

    with open("temp_input.txt", "w") as f:
        f.write(input_str.strip())

    ext = solution_file.split(".")[-1]
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

    return input_str.strip(), output.strip()

def generate_testcases(max_t=100, num_testcases=10):
    print_header("Test Case Generator")

    try:
        solution_file = select_solution()
    except SystemExit:
        return False

    print_success(f"Selected solution: {solution_file}")

    print_success(
        f"Generating {num_testcases} test files with up to {max_t} test cases each..."
    )

    successful_cases = 0

    for i in range(num_testcases):
        try:

            input_data, output_data = generate_test_case(solution_file, max_t)

            with open(f"in{i:02d}.txt", "w") as f:
                f.write(input_data)
            with open(f"out{i:02d}.txt", "w") as f:
                f.write(output_data)

            print_success(f"Generated test case {i:02d}")
            successful_cases += 1

        except Exception as e:
            print_error(f"Failed to generate test case {i:02d}: {str(e)}")

    print_header("Test Case Generation Complete")

    if successful_cases == num_testcases:
        print(
            f"{Fore.GREEN}✨ Generated all {num_testcases} test case files successfully!{Style.RESET_ALL}"
        )
        return True
    else:
        print(
            f"{Fore.YELLOW}⚠️ Generated {successful_cases} out of {num_testcases} test case files{Style.RESET_ALL}"
        )
        return False

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    generate_testcases()
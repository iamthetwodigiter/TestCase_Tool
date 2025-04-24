# Test Case Generator and Validator Tool

A command-line tool for generating and validating competitive programming test cases across multiple programming languages.

## Features

- Generate test cases with customizable parameters
- Validate test cases against solution implementations
- Support for multiple programming languages:
  - Python (.py)
  - Java (.java)
  - C (.c)
  - C++ (.cpp)
- Automatic language support detection
- Detailed validation reports
- Colorized console output
- Both standalone and combined operation modes

## Prerequisites

The tool requires different compilers/runtimes based on the solution language you want to use:

- **Python**: Python 3.x
- **Java**: JDK (Java Development Kit)
- **C**: GCC compiler
- **C++**: G++ compiler

Additional Python dependencies:
```bash
pip install colorama
```

## Project Structure

```
TestCase_Tool/
├── main.py              # Main entry point
├── generate_testcases.py # Test case generation module
├── validate_testcases.py # Test case validation module
└── solution.[py/java/c/cpp] # Your solution implementation
```

## Usage

### Using Python Script

### Basic Command Structure

```bash
python main.py <action> [--max-cases N] [--num-files M]
```

### Arguments

- `action`: Required. Choose from:
  - `generate`: Only generate test cases
  - `validate`: Only validate existing test cases
  - `both`: Generate and validate test cases
- `--max-cases`: Optional. Maximum test cases per file (default: 100)
- `--num-files`: Optional. Number of test files to generate (default: 10)

### Examples

1. Generate 10 test files with up to 100 cases each:
```bash
python main.py generate
```

2. Generate 5 test files with up to 50 cases each:
```bash
python main.py generate --max-cases 50 --num-files 5
```

3. Validate existing test cases:
```bash
python main.py validate
```

4. Generate and immediately validate test cases:
```bash
python main.py both
```

### Using Executable
If you prefer using an executable instead of running Python scripts directly, you can:

1. Download the latest release from the releases page
2. Run the executable using similar command structure:
```batch
testcase_tool.exe <action> [--max-cases N] [--num-files M]
```

Examples using executable:
```batch
testcase_tool.exe generate
testcase_tool.exe validate
testcase_tool.exe both --max-cases 50 --num-files 5
```

Note: The executable version includes all dependencies and doesn't require Python or other language runtimes to be installed (except for the language you want to use for solutions).

## Solution File Requirements

1. Create your solution file with the appropriate extension:
   - Python: `solution.py`
   - Java: `Solution.java`
   - C: `solution.c`
   - C++: `solution.cpp`

2. Your solution should:
   - Read input from standard input (stdin)
   - First line contains T (number of test cases)
   - Each test case contains two integers X and Y
   - Output results to standard output (stdout)

Example Python solution:
```python
def solve(x, y):
    return x + y

T = int(input())
for _ in range(T):
    x, y = map(int, input().split())
    print(solve(x, y))
```

## Output Format

### Generated Files
- Input files: `in00.txt`, `in01.txt`, ...
- Output files: `out00.txt`, `out01.txt`, ...

### Validation Results
The tool provides:
- Pass/fail status for each test case
- Detailed diff for failed cases
- Summary of total passed/failed cases
- Overall validation status

## Error Handling

The tool includes robust error handling for:
- Missing language dependencies
- Invalid solution files
- Runtime errors during generation/validation
- Missing input/output files
- Format mismatches

## Contributors

[Prabhat Jana](https://github.com/iamthetwodigiter)

## Contributing

Feel free to open issues or submit pull requests for:
- Bug fixes
- New features
- Documentation improvements
- Additional language support

## License

This project is open source and available under the MIT License.
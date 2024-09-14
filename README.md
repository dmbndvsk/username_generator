# Username Generator

This Python program generates usernames based on user data from input files. The program processes one or more input files where each line contains user information such as ID, forename, middle name (optional), surname, and department. The generated usernames follow a specific rule and ensure uniqueness by appending numbers to duplicates.

## Features
- **Username generation** based on the first letter of the forename, the middle name (if available), and the first 7 characters of the surname.
- **Handles duplicates** by appending a number to usernames if the same username appears multiple times.
- **Supports multiple input files**.
- **Command-line interface** for processing input files and generating output.

## Prerequisites
To run this project, you need:
- **Python 3.7+**

## Usage

### Command-Line Usage

You can run the program directly from the command line. Here's how you can use the available options:

- **Display Help**:  
  Use the `--help` option to display help information:
  ```bash
  python3 ugen.py --help
  ```

- **Generate Usernames**:  
  To generate usernames from input files and write the results to an output file:
  ```bash
  python3 ugen.py --output <output_file> <input_file1> <input_file2> ...
  ```

#### Example:
```bash
python3 ugen.py --output output.txt test_data/input_file1.txt test_data/input_file2.txt
```

Upon successful execution, you will see:
```
Usernames successfully generated and written to the output file.
```

### Viewing Documentation with `pydoc`

You can view the documentation (docstrings) of the project using `pydoc`. To view the documentation for the `ugen.py` script, run the following command:

```bash
python3 -m pydoc ugen
```

This will display detailed documentation, including descriptions of functions and arguments, based on the docstrings in the script.

### Input File Format
Each line in the input file should contain the following fields separated by colons (`:`):
```
<ID>:<Forename>:<Middle Name (optional)>:<Surname>:<Department>
```

#### Example of Input File:
```
1234:Jozef:Miloslav:Hurban:Legal
4567:Milan:Rastislav:Stefanik:Defence
4563:Jozef::Murgas:Development
1111:Pista::Hufnagel:Sales
```

### Output File Format
The output file contains lines with the following format:
```
<ID>:<Generated Username>:<Forename>:<Middle Name>:<Surname>:<Department>
```

#### Example of Output File:
```
1234:jmhurban:Jozef:Miloslav:Hurban:Legal
4567:mrstefani:Milan:Rastislav:Stefanik:Defence
4563:jmurgas:Jozef::Murgas:Development
1111:phufnage:Pista::Hufnagel:Sales
```

## Running Tests
The project includes unit tests to ensure the correctness of the program. Tests cover the main functionality, such as generating usernames, handling duplicate usernames, and testing for error handling (file not found, IO errors, etc.).

To run the tests, use the following command:
```bash
python3 -m unittest discover
```

### Running Full Test
You can also run a separate script to ensure the output matches expected results using the following:
```bash
python3 test.py ugen.py test_data
```

Upon success, you will see:
```
Test passed successfully!
```

## Handling Errors
- If the input file is not found, an error message will be printed:  
  `Error: File <file_name> not found.`
  
- If the program encounters issues writing to the output file, an error message will be printed:  
  `Error: Could not write to file <output_file>.`

## Known Limitations
- The program does not handle user input validation, such as missing or malformed fields in the input file.
- Input files must be encoded in UTF-8.

import subprocess
import sys
import os


def run_test_case(script_path, data_dir):
    """Runs the program and checks the output against test data."""
    input_file1 = os.path.join(data_dir, 'input_file1.txt')
    input_file2 = os.path.join(data_dir, 'input_file2.txt')
    expected_output_file = os.path.join(data_dir, 'expected_output.txt')

    result = subprocess.run(['python3', script_path, '-o', 'output_test.txt', input_file1, input_file2],
                            capture_output=True, text=True)

    assert result.returncode == 0, "Program failed to run."

    with open('output_test.txt', 'r') as output_file, open(expected_output_file, 'r') as expected_file:
        output_data = output_file.readlines()
        expected_data = expected_file.readlines()

    assert output_data == expected_data, "Test failed: Output does not match expected results!"

    print("Test passed successfully!")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 test.py <script_path> <data_dir>")
        sys.exit(1)

    script_path = sys.argv[1]
    data_dir = sys.argv[2]

    run_test_case(script_path, data_dir)

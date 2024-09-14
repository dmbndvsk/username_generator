import unittest
from ugen import generate_username, handle_duplicates, read_input_files, write_output_file
import os
from unittest.mock import patch, mock_open
import subprocess


class TestUsernameGeneration(unittest.TestCase):

    def test_generate_username_with_middle_name(self):
        """Test username generation with a middle name."""
        result = generate_username('Jozef', 'Miloslav', 'Hurban')
        self.assertEqual(result, 'jmhurban')

    def test_generate_username_without_middle_name(self):
        """Test username generation without a middle name."""
        result = generate_username('Jozef', None, 'Murgas')
        self.assertEqual(result, 'jmurgas')

    def test_generate_username_with_long_surname(self):
        """Test username generation with long surname (limit to 7 characters)."""
        result = generate_username('Jozef', None, 'Verylongsurname')
        self.assertEqual(result, 'jverylon')


class TestHandleDuplicates(unittest.TestCase):

    def test_handle_duplicates_with_no_duplicates(self):
        """Test handling when there are no duplicate usernames."""
        users = [
            {'username': 'jmhurban', 'id': '1234'},
            {'username': 'mrstefan', 'id': '5678'}
        ]
        result = handle_duplicates(users)
        self.assertEqual(result[0]['username'], 'jmhurban')
        self.assertEqual(result[1]['username'], 'mrstefan')

    def test_handle_duplicates_with_duplicates(self):
        """Test handling of duplicate usernames."""
        users = [
            {'username': 'jmhurban', 'id': '1234'},
            {'username': 'jmhurban', 'id': '5678'}
        ]
        result = handle_duplicates(users)
        self.assertEqual(result[1]['username'], 'jmhurban1')


class TestFileOperations(unittest.TestCase):

    def setUp(self):
        """Set up test files."""
        self.input_file = 'test_input.txt'
        self.output_file = 'test_output.txt'
        with open(self.input_file, 'w') as f:
            f.write("1234:Jozef:Miloslav:Hurban:Legal\n")
            f.write("4567:Milan:Rastislav:Stefanik:Defence\n")

    def tearDown(self):
        """Remove test files after tests."""
        if os.path.exists(self.input_file):
            os.remove(self.input_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_read_input_files(self):
        """Test reading from input files."""
        data = read_input_files([self.input_file])
        self.assertEqual(len(data), 2)  # There should be 2 lines
        self.assertEqual(data[0], "1234:Jozef:Miloslav:Hurban:Legal\n")

    def test_write_output_file(self):
        """Test writing to output file."""
        users = [
            {'id': '1234', 'username': 'jmhurban', 'forename': 'Jozef',
                'middle_name': 'Miloslav', 'surname': 'Hurban', 'department': 'Legal'}
        ]
        write_output_file(self.output_file, users)
        with open(self.output_file, 'r') as f:
            content = f.read()
            self.assertIn("1234:jmhurban:Jozef:Miloslav:Hurban:Legal", content)

    @patch('builtins.print')
    def test_file_not_found(self, mock_print):
        """Test reading a non-existent file and checking error message."""
        read_input_files(['non_existent_file.txt'])
        mock_print.assert_called_with(
            'Error: File non_existent_file.txt not found.')

    @patch('builtins.print')
    @patch('builtins.open', side_effect=IOError("Cannot write to file"))
    def test_write_output_file_error(self, mock_open, mock_print):
        """Test writing to file when an IOError occurs."""
        users = [
            {'id': '1234', 'username': 'jmhurban', 'forename': 'Jozef',
                'middle_name': 'Miloslav', 'surname': 'Hurban', 'department': 'Legal'}
        ]
        write_output_file('output_file.txt', users)
        mock_print.assert_called_with(
            "Error: Could not write to file output_file.txt.")


class TestExceptionHandling(unittest.TestCase):

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_read_input_file_not_found(self, mock_open):
        """Test FileNotFoundError in read_input_files."""
        data = read_input_files(['non_existent_file.txt'])
        self.assertEqual(data, [])

    @patch('builtins.print')
    @patch('builtins.open', side_effect=IOError)
    def test_read_input_io_error(self, mock_open, mock_print):
        """Test IOError in read_input_files."""
        data = read_input_files(['corrupt_file.txt'])
        self.assertEqual(data, [])
        mock_print.assert_called_with(
            'Error: Could not read file corrupt_file.txt.')

    @patch('builtins.print')
    @patch('builtins.open', side_effect=IOError)
    def test_write_output_io_error(self, mock_open, mock_print):
        """Test IOError in write_output_file."""
        users = [
            {'id': '1234', 'username': 'jmhurban', 'forename': 'Jozef',
                'middle_name': 'Miloslav', 'surname': 'Hurban', 'department': 'Legal'}
        ]
        write_output_file('output_file.txt', users)
        mock_print.assert_called_with(
            "Error: Could not write to file output_file.txt.")


class TestMainFunction(unittest.TestCase):

    def setUp(self):
        """Set up test files."""
        self.input_file = 'test_input.txt'
        self.output_file = 'test_output.txt'
        with open(self.input_file, 'w') as f:
            f.write("1234:Jozef:Miloslav:Hurban:Legal\n")
            f.write("4567:Milan:Rastislav:Stefanik:Defence\n")

    def tearDown(self):
        """Remove test files after tests."""
        if os.path.exists(self.input_file):
            os.remove(self.input_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_main_function(self):
        """Test running the program with arguments."""
        result = subprocess.run(['python3', 'ugen.py', '--output', self.output_file, self.input_file],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists(self.output_file))

        with open(self.output_file, 'r') as f:
            content = f.read()
            self.assertIn("1234:jmhurban:Jozef:Miloslav:Hurban:Legal", content)

    def test_no_arguments(self):
        """Test running the program without arguments."""
        result = subprocess.run(['python3', 'ugen.py'],
                                capture_output=True, text=True)
        self.assertIn("usage", result.stderr)
        self.assertNotEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()

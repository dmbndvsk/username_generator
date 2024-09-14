import argparse


def read_input_files(file_paths):
    """
    Reads user data from one or more input files.

    Args:
        file_paths (list): List of file paths to read from.

    Returns:
        list: List of user data from all input files.
    """
    data = []
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                file_data = file.readlines()
                data.extend(file_data)
        except FileNotFoundError:
            print(f"Error: File {file_path} not found.")
        except IOError:
            print(f"Error: Could not read file {file_path}.")
    return data


def generate_username(forename, middle_name, surname):
    """
    Generates a username from forename, middle name, and surname.

    Args:
        forename (str): User's forename.
        middle_name (str or None): User's middle name (optional).
        surname (str): User's surname.

    Returns:
        str: Generated username, limiting the surname to 7 characters if longer.
    """
    username = forename[0].lower()
    if middle_name:
        username += middle_name[0].lower()
    username += surname[:7].lower()
    return username


def handle_duplicates(users):
    """
    Handles duplicate usernames by appending a number if duplicates are found.

    Args:
        users (list): List of user dictionaries with generated usernames.

    Returns:
        list: List of users with unique usernames.
    """
    seen = {}
    for user in users:
        username = user['username']
        if username in seen:
            seen[username] += 1
            user['username'] = f"{username}{seen[username]}"
        else:
            seen[username] = 0
    return users


def write_output_file(output_file, users):
    """
    Writes user data to the specified output file.

    Args:
        output_file (str): Path to the output file.
        users (list): List of user dictionaries to write to the file.
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            for user in users:
                middle_name = user['middle_name'] if user['middle_name'] is not None else ''
                line = f"{user['id']}:{user['username']}:{user['forename']}:{
                    middle_name}:{user['surname']}:{user['department']}\n"
                file.write(line)
    except IOError:
        print(f"Error: Could not write to file {output_file}.")


def main():
    """
    Main function to handle command-line arguments, read input files,
    process user data, generate usernames, handle duplicates, and write output to a file.
    """
    parser = argparse.ArgumentParser(
        description='Generate usernames from input files.')
    parser.add_argument('-o', '--output', required=True,
                        help='Output file path')
    parser.add_argument('input_files', nargs='+', help='Input file paths')
    args = parser.parse_args()

    data = read_input_files(args.input_files)

    users = []
    for line in data:
        fields = line.strip().split(':')
        if len(fields) >= 5:
            user = {
                'id': fields[0],
                'forename': fields[1],
                'middle_name': fields[2] if fields[2] else None,
                'surname': fields[3],
                'department': fields[4],
                'username': generate_username(fields[1], fields[2], fields[3])
            }
            users.append(user)

    users = handle_duplicates(users)

    write_output_file(args.output, users)

    print("Usernames successfully generated and written to the output file.")


if __name__ == '__main__':
    main()

import os

def get_file_lines(calling_file, file_str):
    path = os.path.join(os.path.dirname(calling_file), file_str)
    with open(path, 'r+b') as f:
        decoded_file = f.read().decode('UTF-8').splitlines()

    return decoded_file

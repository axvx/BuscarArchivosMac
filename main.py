#Script para buscar archivos en MAC

import os
import concurrent.futures
from urllib.parse import quote


def find_files_fast(directory="/"):
    """Recursively finds JPEG files in a given directory using concurrent processing.

    Args:
        directory: The directory to start searching from.

    Returns:
        A list of paths to found JPEG files.
    """
    type_files = []
    permission_denied_paths = []  # To keep track of permission denied paths

    def scan_dir(directory):
        try:
            with os.scandir(directory) as entries:
                for entry in entries:
                    if entry.is_symlink():  # Skip symbolic links
                        continue
                    if entry.is_dir():
                        try:
                            scan_dir(entry.path)
                        except PermissionError:
                            permission_denied_paths.append(entry.path)
                            continue
                    elif entry.is_file() and entry.name.endswith(".java"):
                        filepath = entry.path
                        type_files.append(filepath)
                        # Encode the path to handle special characters and spaces
                        encoded_path = quote(filepath)
                        # Print as a clickable URL if supported by the terminal
                        print(f"file://{encoded_path}")
        except PermissionError:
            permission_denied_paths.append(directory)

    # Use ThreadPoolExecutor to handle multiple directories concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(scan_dir, directory)
        future.result()  # Wait for the directory scanning to complete

    # Optionally, display or log the permission denied paths for review or debugging
    # for path in permission_denied_paths:
    #     print(f"Permission denied (logged): {path}")

    return type_files


# Example usage:
find_files = find_files_fast()
print(find_files)
import os
from typing import Generator

def load_wordlist_stream(file_path: str, chunk_size: int = 1024 * 1024) -> Generator[str, None, None]:
    """
    Reads a wordlist file efficiently by streaming chunks of data from disk,
    handling large files without consuming excessive memory. Yields stripped,
    non-empty strings suitable for subdomain brute-forcing.

    Args:
        file_path (str): The path to the wordlist file on disk.
        chunk_size (int): The size of the buffer read into memory (default: 1MB).

    Yields:
        Generator[str, None, None]: Individual lines (words) from the wordlist.

    Raises:
        FileNotFoundError: If the specified wordlist file does not exist.
        PermissionError: If there are insufficient permissions to read the file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The wordlist file at '{file_path}' was not found.")
        
    if not os.path.isfile(file_path):
        raise ValueError(f"The path '{file_path}' is not a valid file.")

    remainder = ""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            
            lines = (remainder + chunk).splitlines(keepends=True)
            
            if lines and not lines[-1].endswith(("\n", "\r")):
                remainder = lines.pop()
            else:
                remainder = ""
                
            for line in lines:
                clean_line = line.strip()
                if clean_line:
                    yield clean_line
                    
        if remainder:
            clean_remainder = remainder.strip()
            if clean_remainder:
                yield clean_remainder
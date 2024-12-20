"""
Module for managing test scripts.
"""

from src.utils import get_full_path  # type: ignore

if __name__ == "__main__":
    p = get_full_path("../data")
    print(p)

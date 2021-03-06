"""
deletes all the reader output files
generated by the application
"""
import os
import glob

FILENAMES = glob.glob("*.out.txt")
for file in FILENAMES:
    try:
        os.remove(file)
    except FileNotFoundError:
        print("No File to Delete")

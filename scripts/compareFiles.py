import os

ORGINAL_FILES_PATH = "docs/docs3"
SPLIT_FILES_PATH = "docs/udyan"

# print names of PDF files in ORGINAL_FILES_PATH but not in SPLIT_FILES_PATH
def compare_files():
    original_files = os.listdir(ORGINAL_FILES_PATH)
    split_files = os.listdir(SPLIT_FILES_PATH)
    for file in original_files:
        if file.endswith(".pdf") and file not in split_files:
            print(file)


compare_files()
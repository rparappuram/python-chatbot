# LangChain's DirectoryLoader uses an UnstructuredLoader under the hood
# Given a directory with files and subdirectories, 
# write a program that will remove any unsupported file types.

# The supported file types are:
# .csv, .eml, .msg, .epub, .xlsx, .xls, .html,
# .png, .jpg, .md, .odt, .pdf, .txt, .ppt, .pptx, 
# .rtf, .doc, .docx, .xml

import os
import shutil
from pathlib import Path

# list of supported file types
supported_file_types = [
    ".csv", ".eml", ".msg", ".epub", ".xlsx", ".xls", ".html",
    ".png", ".jpg", ".md", ".odt", ".pdf", ".txt", ".ppt", ".pptx",
    ".rtf", ".doc", ".docx", ".xml"
]

# list of unsupported file types
unsupported_file_types = [".DS_Store", ".yaml", ".mdx", ".svg", ".ini", ".numbers", ".jpeg"]

# path to directory
path = "docs/AIAssistent_Data"

# iterate through directory
for root, dirs, files in os.walk(path):
    for file in files:
        # get file extension
        file_type = os.path.splitext(file)[1].lower()
        # if file extension in unsupported file types
        if file_type in unsupported_file_types:
            # remove file
            os.remove(os.path.join(root, file))

# iterate through directory
for root, dirs, files in os.walk(path):
    for file in files:
        # get file extension
        file_type = os.path.splitext(file)[1].lower()
        # if file extension in unsupported file types
        if file_type not in supported_file_types:
            # remove file and print path
            os.remove(os.path.join(root, file))
            print(f"Removed: ", os.path.join(root, file)[22:])

# iterate through directory
for root, dirs, files in os.walk(path):
    for dir in dirs:
        # if directory is empty
        if not os.listdir(os.path.join(root, dir)):
            # remove directory
            shutil.rmtree(os.path.join(root, dir))
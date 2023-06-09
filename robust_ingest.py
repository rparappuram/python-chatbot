import docx
import pandas as pd
import chardet
from pdfminer.high_level import extract_text
import os
import tiktoken


encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")


def read_pdf(file_path):
    try:
        text = extract_text(file_path)
    except Exception as e:
        print(f"Error reading PDF file {file_path}: {str(e)}")
        text = ""
    return text


def read_docx(file_path):
    try:
        doc = docx.Document(file_path)
        text = " ".join([p.text for p in doc.paragraphs])
    except Exception as e:
        print(f"Error reading DOCX file {file_path}: {str(e)}")
        text = ""
    return text


def read_xlsx_file(file_path):
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error reading XLSX file {file_path}: {str(e)}")
        df = None

    file_name = os.path.basename(file_path)
    return file_name, df


def read_csv_file(file_path):
    try:
        with open(file_path, "rb") as f:
            encoding = chardet.detect(f.read())["encoding"]
        df = pd.read_csv(file_path, encoding=encoding)
    except Exception as e:
        print(f"Error reading CSV file {file_path}: {str(e)}")
        df = None

    file_name = os.path.basename(file_path)
    return file_name, df


def read_txt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading TXT file {file_path}: {str(e)}")
        text = ""
    return text


def process_table_file(file_path):
    def count_tokens(text):
        tokens = len(encoding.encode(text))
        return tokens

    file_ext = os.path.splitext(file_path)[1].lower()

    if file_ext == ".csv":
        file_name, df = read_csv_file(file_path)
    elif file_ext == ".xlsx":
        file_name, df = read_xlsx_file(file_path)
    else:
        raise ValueError(
            "Unsupported file extension. Please provide a CSV or XLSX file."
        )

    if df is None:
        return None

    plain_csv_text = df.to_csv(index=False)
    rows = plain_csv_text.split("\n")

    chunk_tokens = 0
    chunks = []
    chunk = ""

    for row in rows:
        row_tokens = len(encoding.encode(row))
        chunk_tokens += row_tokens

        if chunk_tokens >= 1000:
            chunks.append(chunk)
            chunk = ""
            chunk_tokens = row_tokens

        chunk += "\n" + row

    # Add the remaining chunk, if any
    if chunk:
        chunks.append(chunk)

    chunks = [f"{file_name}\n{chunk}" for chunk in chunks]

    return chunks


def ingester(file_path):
    extension = file_path.split(".")[-1].lower()
    if extension == "pdf":
        return read_pdf(file_path)
    elif extension in ["doc", "docx"]:
        return read_docx(file_path)
    elif extension in ["csv", "xlsx"]:
        return process_table_file(file_path)
    elif extension == "txt":
        return read_txt(file_path)
    else:
        print(f"Unsupported file type: {extension}")
        return ""


def chunk_text(text, chunk_size=1000):
    words = text.split()
    chunks = []
    current_chunk = ""

    for word in words:
        # Check if adding the word to the current chunk would exceed the chunk size
        if len(current_chunk) + len(word) + 1 > chunk_size:
            # If so, add the current chunk to the chunks list and start a new chunk with the current word
            chunks.append(current_chunk.strip())
            current_chunk = word
        else:
            # Otherwise, add the word to the current chunk
            current_chunk += f" {word}"

    # Add the last chunk to the chunks list
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def ingest_folder(folder_path, progress=True):
    context_chunks = []

    # List all files in the folder
    file_paths = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]
    total_files = len(file_paths)

    for i, file_path in enumerate(file_paths):
        if progress:
            print(f"Processing {file_path}")

        text = ingester(file_path)

        if isinstance(text, str):
            chunks = chunk_text(text)
            context_chunks.extend(chunks)

        else:
            context_chunks.extend(text)

    return context_chunks

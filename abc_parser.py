import os
from typing import List, Dict
from configurations import BOOKS_DIR

def parse_abc_file(file_path: str) -> List[Dict]:
    """
    Read one .abc file and extract all tunes inside it.

    Each tune:
      - starts with 'X:'
      - optionally has T:, R:, M:, K:
      - then has a body (music notation)
    Returns a list of dictionaries, one per tune.
    """
    tunes = []
    current_tune = None
    body_lines: List[str] = []

    book_name = os.path.basename(os.path.dirname(file_path))
    filename = os.path.basename(file_path)

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for raw_line in f:
            line = raw_line.strip()

            if line.startswith("X:"):
                # save previous tune if exists
                if current_tune is not None:
                    current_tune["body"] = "\n".join(body_lines).strip()
                    tunes.append(current_tune)

                current_tune = {
                    "book": book_name,
                    "filename": filename,
                    "X": line[2:].strip(),
                    "T": "",
                    "R": "",
                    "M": "",
                    "K": "",
                    "body": ""
                }
                body_lines = []
            elif current_tune is not None:
                if line.startswith("T:"):
                    title = line[2:].strip()
                    if current_tune["T"]:
                        current_tune["T"] += " / " + title
                    else:
                        current_tune["T"] = title
                elif line.startswith("R:"):
                    current_tune["R"] = line[2:].strip()
                elif line.startswith("M:"):
                    current_tune["M"] = line[2:].strip()
                elif line.startswith("K:"):
                    current_tune["K"] = line[2:].strip()
                else:
                    body_lines.append(line)

    if current_tune is not None:
        current_tune["body"] = "\n".join(body_lines).strip()
        tunes.append(current_tune)

    return tunes
# Data Centric Programming Assignment 2025

- [Assignment Brief](assignment.md)

Name: Lea Stanisavljevic

Student Number: A00046044

# Screenshots

# Description of the project
This project is a small data-processing application built for the Data Centric Programming module (DATA2005).
Its main goal is to take a collection of traditional music files written in ABC notation, extract all of the individual tunes, store them in a databas and then allow the user to browse, search and analyse the tunes in an interface.

It is written in python. It uses SQLite and MySQL for the database of teh tunes. It has a simple Tkinter GUI for the user to query the database without needing to use the terminal. The GUI displays results in an output window using stdout so the same backend functions work both in console mode and in the GI.

Main Features
- file parsing
- a database
- SQL querying
- data analysis using pandas
- basic gui design

# Instructions for use
1. **Clone the repository** from GitHub.  
2. Install **Python 3**, then create a virtual environment.  
3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Place the ABC music folders inside the `abc_books/` directory.  
5. Run the program:

    ```bash
    python main.py
    ```

6. The GUI will open automatically.
**(or just press the 'run python file' in VS Code)**

### Using the GUI

Use the buttons on the left to:

- rebuild the database  
- list the first 20 tunes  
- search by title  
- search by key signature  
- search by meter  
- view full tune details  
- run pandas analysis  
- switch between SQLite and MySQL  
- close the window

# How it works:
### 1. Parsing the ABC files

All `.abc` files inside `abc_books/` are scanned and parsed.

A tune begins with `X:` and may include:

- `T:` title  
- `R:` rhythm  
- `M:` meter  
- `K:` key signature  

The parser extracts all metadata and body text into a Python dictionary.

### 2. Database Storage

After parsing, tunes can be inserted into:

- **SQLite** (`tunes.db`)  
- **MySQL** (via credentials stored in `.env`)  

Both backends use the same table structure.

### 3. Querying the Tunes

Several query functions are provided:

- list the first 20 tunes  
- search by title  
- search by key signature  
- search by meter  
- show all tune details  

### 4. Data Analysis with pandas

The tunes table can be loaded into a pandas DataFrame for:

- tune counts per book  
- most common keys  
- meter and rhythm distribution  
- filtering by type or keyword  

### 5. Graphical User Interface

The interface is built with **Tkinter**.

Printed output is redirected into a scrollable Text widget using:

```python
contextlib.redirect_stdout
```

This prevents code duplication and the data is only displayed in the gui.

# List of files in the project

| Files | Source |
|-----------|-----------|
| main.py | Self written |
| db_connection.py | Modified from [reference]() |
| db_analysis.py | Modified from [reference]() |
| db_gui.py | Modified from [reference]() |
| db_query.py | Modified from [reference]() |
| abc_parser.py | Modified from [reference]() |
| abc_books | Provided by lecturer |
| tunes.db | Provided by lecturer |
| requirements.txt | Self written |
| .venv/venv | Self written |

# References
* Item 1
* Item 2

# What I am most proud of in the assignment

Bla bla bla

# What I learned
- How to parse structured text formats (ABC notation)  
- How to build and manage SQLite and MySQL databases in Python  
- How to use pandas for data analysis  
- How to build an event-driven GUI in Tkinter  
- How to design a modular and maintainable project  

This project helped me connect data parsing, databases, analysis and user interfaces into one application where is all works together.
# Task 3: Automated File Organizer & Cleanup Utility

A command-line tool that sorts the files in a folder into sub-folders by type
(Images, Documents, Spreadsheets, Videos, Audio, Archives, Code, Installers, Others).
Python 3, standard library only (`os`, `shutil`, `argparse`).

## Features
- Safe by default: running without `--apply` only previews what would move
- Groups files by extension into category folders
- Never overwrites: duplicate names become `photo (1).jpg`, `photo (2).jpg`
- Skips sub-folders and hidden files
- Optional `--clean-empty` removes empty folders afterwards
- Prints a summary of how many files went to each category

## Usage
```
python file_organizer.py
python file_organizer.py "C:/Users/me/Downloads"
python file_organizer.py "C:/Users/me/Downloads" --apply
python file_organizer.py "C:/Users/me/Downloads" --apply --clean-empty
```

## Customising
Edit the `CATEGORIES` dictionary at the top of `file_organizer.py` to add or change file types.

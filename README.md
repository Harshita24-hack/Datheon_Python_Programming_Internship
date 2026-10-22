# Datheon Python Programming Internship

Projects completed for the Datheon Python Programming Internship (Batch 01).

**Author:** Harshita Sharma

## Task 1: Hangman Game (`hangman.py`)
A console word-guessing game with ASCII gallows art.
- Random secret word, masked display (e.g. `_ R E A _`)
- 6 allowed mistakes, repeated guesses not penalised
- Win and game-over screens, play-again option

Run: `python hangman.py`

## Task 3: File Organizer (`file_organizer.py`)
Sorts the files in a folder into sub-folders by type (Images, Documents, etc.).
- Safe preview mode by default; add `--apply` to move files
- Never overwrites duplicate names
- Optional `--clean-empty` removes empty folders

Run: `python file_organizer.py "C:/path/to/folder" --apply`

## Task 4: Terminal Chatbot (`chatbot.py`)
A rule-based assistant that recognises multiple intents.
- Greets you, remembers your name, tells time/date, jokes and facts
- Solves simple maths, shows help, says goodbye

Run: `python chatbot.py`

## Requirements
Python 3, standard library only. No installs needed.

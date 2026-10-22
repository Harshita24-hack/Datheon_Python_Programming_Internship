"""Hangman - a console word guessing game.

Run:  python hangman.py
Optional: put the downloaded English word list next to this file as
'words.txt' (one word per line). If it's missing, a built-in list is used.
"""

import os
import random

MAX_MISTAKES = 6
MIN_WORD_LEN = 5
MAX_WORD_LEN = 10

# Words from big scraped lists can include spam or adult terms; skip these.
BLOCKLIST = {
    "phentermine", "viagra", "cialis", "levitra", "xanax", "tramadol",
    "valium", "ambien", "zoloft", "prozac", "adipex", "fioricet",
    "hydrocodone", "casino", "poker", "porn", "naked", "sexual", "lesbian",
    "lesbians", "lingerie", "fetish", "spank", "spanking", "nudist",
    "erotica", "escorts", "blackjack", "roulette", "gambling", "cigarette",
    "cigarettes", "tobacco", "alcohol", "abortion", "suicide", "torture",
}

FALLBACK_WORDS = [
    "python", "keyboard", "program", "variable", "function", "console",
    "library", "network", "monitor", "internet", "developer", "software",
    "algorithm", "database", "compiler", "terminal", "package", "module",
    "project", "challenge", "elephant", "mountain", "football", "chocolate",
]

# One ASCII picture per number of mistakes (0 to 6).
STAGES = [
    """
      +---+
      |   |
          |
          |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
          |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
     / \\  |
          |
    =========""",
]


def load_words(path="words.txt"):
    """Load and clean the word list; fall back to the built-in list."""
    here = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(here, path)
    words = []
    if os.path.exists(full_path):
        with open(full_path, encoding="utf-8") as f:
            for line in f:
                w = line.strip().lower()
                if (
                    w.isalpha()
                    and MIN_WORD_LEN <= len(w) <= MAX_WORD_LEN
                    and w not in BLOCKLIST
                ):
                    words.append(w)
    return words if words else FALLBACK_WORDS


def masked(word, guessed):
    """Return the word with unguessed letters hidden, e.g. '_ A _ H O N'."""
    return " ".join(ch.upper() if ch in guessed else "_" for ch in word)


def get_guess(guessed):
    """Ask until the player enters one new letter."""
    while True:
        guess = input("Guess a letter: ").strip().lower()
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter (a-z).")
        elif guess in guessed:
            print(f"You already guessed '{guess.upper()}'. No penalty, try again.")
        else:
            return guess


def play_round(word):
    guessed = set()
    mistakes = 0

    while mistakes < MAX_MISTAKES and not set(word) <= guessed:
        print(STAGES[mistakes])
        print(f"\nWord:    {masked(word, guessed)}")
        wrong = sorted(g for g in guessed if g not in word)
        print(f"Wrong:   {' '.join(l.upper() for l in wrong) or '-'}")
        print(f"Lives:   {MAX_MISTAKES - mistakes}\n")

        guess = get_guess(guessed)
        guessed.add(guess)
        if guess in word:
            print(f"Nice! '{guess.upper()}' is in the word.")
        else:
            mistakes += 1
            print(f"Nope, '{guess.upper()}' is not in the word.")

    print(STAGES[mistakes])
    if set(word) <= guessed:
        print("\n" + "=" * 36)
        print("   YOU WIN!  The word was:", word.upper())
        print("=" * 36)
    else:
        print("\n" + "=" * 36)
        print("   GAME OVER.  The word was:", word.upper())
        print("=" * 36)


def main():
    words = load_words()
    print("=== HANGMAN ===")
    print(f"Guess the word before the drawing is complete ({MAX_MISTAKES} mistakes allowed).")
    while True:
        play_round(random.choice(words))
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()

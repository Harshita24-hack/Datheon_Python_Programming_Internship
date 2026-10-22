"""Rule-Based Interactive Terminal Assistant (Chatbot).

Recognises several intents (greeting, time, date, jokes, maths, name, help,
goodbye) using keyword matching. Standard library only.

Run:  python chatbot.py
"""

import random
import re
from datetime import datetime

# Canned responses the bot can pick from
JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why did the Python programmer need glasses? He couldn't C.",
    "There are 10 kinds of people: those who understand binary and those who don't.",
    "A SQL query walks into a bar, walks up to two tables and asks: 'Can I join you?'",
]

FACTS = [
    "Python was named after Monty Python, not the snake.",
    "The first computer bug was a real moth found in a Harvard computer in 1947.",
    "Python was first released in 1991 by Guido van Rossum.",
]

# Each intent: (name, keywords/phrases). The first intent that matches wins,
# so more specific ones are listed earlier.
INTENTS = [
    ("goodbye", ["bye", "goodbye", "exit", "quit", "see you", "cya"]),
    ("greeting", ["hello", "hi", "hey", "good morning", "good evening", "namaste"]),
    ("how_are_you", ["how are you", "how are you doing", "whats up", "how do you do"]),
    ("name", ["your name", "who are you", "what are you"]),
    ("time", ["time", "clock"]),
    ("date", ["date", "day", "today"]),
    ("joke", ["joke", "funny", "laugh"]),
    ("fact", ["fact", "fun fact", "tell me something"]),
    ("thanks", ["thanks", "thank you", "thx"]),
    ("help", ["help", "what can you do", "commands"]),
]


class ChatBot:
    def __init__(self, name="PyBot"):
        self.name = name
        self.user_name = None  # filled in when the user tells us their name

    @staticmethod
    def normalize(text):
        """Lower-case the text and drop punctuation (keeps maths symbols)."""
        return re.sub(r"[^a-z0-9+\-*/%.() ]", "", text.lower()).strip()

    @staticmethod
    def has_phrase(text, phrase):
        """True if `phrase` appears as whole word(s), so 'hi' doesn't match 'this'."""
        return re.search(rf"\b{re.escape(phrase)}\b", text) is not None

    def detect_intent(self, text):
        """Return the first intent whose keywords appear in the text, else None."""
        for intent, phrases in INTENTS:
            if any(self.has_phrase(text, p) for p in phrases):
                return intent
        return None

    @staticmethod
    def try_math(text):
        """Evaluate simple arithmetic like '12 * (3 + 4)'; return None if not maths."""
        expr = text
        # Remove filler words so "calculate 2+2" becomes "2+2"
        for word in ("calculate", "what is", "whats", "solve", "compute"):
            expr = expr.replace(word, "")
        expr = expr.strip()
        # Must contain a digit and only digits/operators/brackets
        if not re.search(r"\d", expr) or not re.fullmatch(r"[0-9+\-*/%.() ]+", expr):
            return None
        if not re.search(r"[+\-*/%]", expr):
            return None
        # Block powers and very long input so nothing can hang the program
        if "**" in expr or len(expr) > 40:
            return "Please keep the maths simple (no powers, short expressions)."
        try:
            # Safe here: the text can only contain digits and operators
            result = eval(expr, {"__builtins__": {}}, {})
        except (SyntaxError, ZeroDivisionError, ValueError):
            return "I couldn't work that out. Check the expression (and no dividing by zero!)."
        return f"The answer is {round(result, 4) if isinstance(result, float) else result}."

    def remember_name(self, raw):
        """Detect 'my name is X' / 'I am X' / 'call me X' and store the name."""
        m = re.search(r"\b(?:my name is|i am|i'm|call me)\s+([A-Za-z]+)", raw, re.I)
        if m:
            self.user_name = m.group(1).capitalize()
            return f"Nice to meet you, {self.user_name}!"
        return None

    def respond(self, raw):
        """Work out the best reply for one line of user input."""
        text = self.normalize(raw)
        if not text:
            return "Say something and I'll respond!"

        # 1) Did the user tell us their name?
        reply = self.remember_name(raw)
        if reply:
            return reply
        if self.has_phrase(text, "my name") and self.user_name:
            return f"Your name is {self.user_name}."

        # 2) Is it a maths question?
        math = self.try_math(text)
        if math:
            return math

        # 3) Otherwise match an intent and look up the reply
        intent = self.detect_intent(text)
        now = datetime.now()
        who = f", {self.user_name}" if self.user_name else ""
        responses = {
            "greeting": f"Hello{who}! How can I help you today?",
            "how_are_you": "I'm just a program, but I'm running great. Thanks for asking!",
            "name": f"I'm {self.name}, a rule-based terminal assistant written in Python.",
            "time": f"The time is {now.strftime('%I:%M %p')}.",
            "date": f"Today is {now.strftime('%A, %d %B %Y')}.",
            "joke": random.choice(JOKES),
            "fact": random.choice(FACTS),
            "thanks": "You're welcome!",
            "help": (
                "I can: greet you, tell the time and date, tell jokes and facts, "
                "do maths (try '12 * (3 + 4)'), and remember your name "
                "(say 'my name is ...'). Type 'bye' to quit."
            ),
            "goodbye": f"Goodbye{who}! Have a great day.",
        }
        # Fallback when nothing matched
        return responses.get(intent, "Sorry, I didn't understand that. Type 'help' to see what I can do.")

    def is_goodbye(self, raw):
        """True when the user wants to leave."""
        return self.detect_intent(self.normalize(raw)) == "goodbye"


def main():
    bot = ChatBot()
    print(f"=== {bot.name} ===  (type 'help' for options, 'bye' to quit)")
    while True:
        try:
            raw = input("You: ")
        except (EOFError, KeyboardInterrupt):  # Ctrl+D / Ctrl+C exit cleanly
            print(f"\n{bot.name}: Goodbye!")
            break
        print(f"{bot.name}: {bot.respond(raw)}")
        if bot.is_goodbye(raw):
            break


# Only run when executed directly
if __name__ == "__main__":
    main()
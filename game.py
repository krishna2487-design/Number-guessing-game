

import json
import os
import random
import time

HIGH_SCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "high_scores.json")

DIFFICULTIES = {
    "1": ("Easy", 10),
    "2": ("Medium", 5),
    "3": ("Hard", 3),
}


def load_high_scores():
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_high_scores(scores):
    try:
        with open(HIGH_SCORE_FILE, "w") as f:
            json.dump(scores, f, indent=2)
    except IOError:
        print("(Note: could not save high scores to disk.)")


def print_welcome():
    print("=" * 50)
    print("   Welcome to the Number Guessing Game!")
    print("=" * 50)
    print("I'm thinking of a number between 1 and 100.")
    print("Guess it correctly before you run out of chances!")
    print("Tip: after a wrong guess, you'll be told if the")
    print("     number is higher or lower than your guess.")
    print("     Type 'hint' at any guess prompt for a clue.")
    print("-" * 50)


def choose_difficulty():
    print("\nPlease select the difficulty level:")
    print("1. Easy   (10 chances)")
    print("2. Medium (5 chances)")
    print("3. Hard   (3 chances)")

    while True:
        choice = input("Enter your choice (1/2/3): ").strip()
        if choice in DIFFICULTIES:
            name, chances = DIFFICULTIES[choice]
            print(f"\nGreat! You have selected the {name} difficulty level.")
            print("Let's start the game!\n")
            return name, chances
        print("Invalid choice. Please enter 1, 2, or 3.")


def get_hint(secret, guess, hints_used):
    """Return a hint string. Hints get progressively more specific."""
    hints_used += 1
    if hints_used == 1:
        parity = "even" if secret % 2 == 0 else "odd"
        return f"Hint: the number is {parity}.", hints_used
    elif hints_used == 2:
        return f"Hint: the number is {'divisible by 5' if secret % 5 == 0 else 'not divisible by 5'}.", hints_used
    else:
        diff = abs(secret - guess)
        if diff <= 5:
            closeness = "very close"
        elif diff <= 15:
            closeness = "fairly close"
        else:
            closeness = "not close"
        return f"Hint: your last guess was {closeness} to the number.", hints_used


def get_valid_guess():
    while True:
        raw = input("Enter your guess (or 'hint'): ").strip().lower()
        if raw == "hint":
            return "hint"
        try:
            value = int(raw)
            if value < 1 or value > 100:
                print("Please guess a number between 1 and 100.")
                continue
            return value
        except ValueError:
            print("That's not a valid number. Try again.")


def play_round(difficulty_name, chances, high_scores):
    secret = random.randint(1, 100)
    attempts = 0
    hints_used = 0
    last_guess = None
    start_time = time.time()

    while attempts < chances:
        remaining = chances - attempts
        print(f"Chances remaining: {remaining}")
        guess = get_valid_guess()

        if guess == "hint":
            hint_text, hints_used = get_hint(secret, last_guess if last_guess else 50, hints_used)
            print(hint_text)
            continue

        attempts += 1
        last_guess = guess

        if guess == secret:
            elapsed = time.time() - start_time
            print(f"\nCongratulations! You guessed the correct number in {attempts} attempts.")
            print(f"Time taken: {elapsed:.1f} seconds.")

            best = high_scores.get(difficulty_name)
            if best is None or attempts < best:
                high_scores[difficulty_name] = attempts
                save_high_scores(high_scores)
                print(f"New high score for {difficulty_name} difficulty: {attempts} attempts!")
            else:
                print(f"Best score for {difficulty_name} difficulty: {best} attempts.")
            return True
        elif guess < secret:
            print(f"Incorrect! The number is greater than {guess}.\n")
        else:
            print(f"Incorrect! The number is less than {guess}.\n")

    print(f"\nSorry, you're out of chances! The number was {secret}.")
    return False


def main():
    print_welcome()
    high_scores = load_high_scores()

    while True:
        difficulty_name, chances = choose_difficulty()
        play_round(difficulty_name, chances, high_scores)

        if high_scores:
            print("\nCurrent high scores (fewest attempts):")
            for level in ("Easy", "Medium", "Hard"):
                if level in high_scores:
                    print(f"  {level}: {high_scores[level]} attempts")

        again = input("\nWould you like to play again? (y/n): ").strip().lower()
        if again != "y":
            print("\nThanks for playing! Goodbye.")
            break
        print()


if __name__ == "__main__":
    main()

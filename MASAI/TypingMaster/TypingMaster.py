import random
import time
import json

# Global Variables
word_list = []  # List to store words for typing test
leaderboard = []  # List to store leaderboard data

# Function to update and sort the leaderboard
def update_leaderboard(username, wpm):
    try:
        # Load existing leaderboard data
        with open("leaderboard.json", "r") as file:
            leaderboard = json.load(file)
    except FileNotFoundError:
        # If the file is not found, initialize an empty leaderboard
        leaderboard = []

    # Add the new entry
    leaderboard.append({"username": username, "wpm": wpm})

    # Sort the leaderboard based on WPM in descending order
    leaderboard = sorted(leaderboard, key=lambda x: x["wpm"], reverse=True)

    # Save the updated leaderboard
    with open("leaderboard.json", "w") as file:
        json.dump(leaderboard, file)


# Function to show the leaderboard
def show_leaderboard():
    with open("leaderboard.json", "r") as file:
        leaderboard = json.load(file)
        print("Leaderboard:")
        for entry in leaderboard:
            print(f"{entry['username']} - {entry['wpm']} WPM")

# Function to load words from a JSON file
def load_words_from_json(category):
    with open("words.json", "r") as file:
        words_data = json.load(file)
        return words_data.get(category, [])

# Function to get user input from the terminal
def get_user_input():
    return input("Type the words exactly as shown. Press 'Ctrl + Q' to quit.\n")

# Function containing the main game logic
def main():
    print("Welcome to Terminal Typing Master!")
    username = input("Enter your username: ")

    while True:
        print("\nOptions:")
        print("1. Start Typing Test")
        print("2. Show Leaderboard")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            category = input("Enter the typing category: ")
            word_list = load_words_from_json(category)
            start_time = time.time()

            print("Random Words:")
            for word in word_list:
                print(word, end=' ', flush=True)
                time.sleep(0.5)  # Adjust as needed
            print("\n")

            user_input = get_user_input()

            end_time = time.time()
            time_taken = end_time - start_time
            words_typed = len(user_input.split())
            wpm = (words_typed / time_taken) * 60  # Calculate WPM

            update_leaderboard(username, wpm)
            print(f"Your WPM: {wpm:.2f}")

        elif choice == "2":
            show_leaderboard()

        elif choice == "3":
            print("Exiting Terminal Typing Master. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()

# Rock, Paper, Scissors Game with Colors by You ❤️

import random
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

print(Fore.YELLOW + "👋 Welcome to Rock, Paper, Scissors Game!")

# Score variables
user_score = 0
computer_score = 0

# Choices
options = ["rock", "paper", "scissors"]

while True:
    print()
    user_choice = input(Fore.YELLOW + "Choose Rock, Paper, or Scissors: ").lower()

    if user_choice not in options:
        print(Fore.RED + "❌ Invalid choice. Try again.")
        continue

    computer_choice = random.choice(options)

    print(f"\n🧍 You chose: {Fore.YELLOW + user_choice}")
    print(f"💻 Computer chose: {Fore.MAGENTA + computer_choice}")

    # Game logic
    if user_choice == computer_choice:
        print(Fore.CYAN + "🤝 It's a tie!")
    elif (
        (user_choice == "rock" and computer_choice == "scissors") or
        (user_choice == "scissors" and computer_choice == "paper") or
        (user_choice == "paper" and computer_choice == "rock")
    ):
        print(Fore.GREEN + "✅ You win this round!")
        user_score += 1
    else:
        print(Fore.RED + "❌ You lose this round!")
        computer_score += 1

    # Display scores
    print(Fore.YELLOW + f"\n🔢 Score - You: {user_score} | Computer: {computer_score}")

    # Ask to continue
    play_again = input(Fore.CYAN + "\nDo you want to play again? (yes/no): ").lower()
    if play_again != "yes":
        print(Fore.MAGENTA + "\n🎮 Thanks for playing! Final Score:")
        print(Fore.YELLOW + f"🙋 You: {user_score}  💻 Computer: {computer_score}")
        break

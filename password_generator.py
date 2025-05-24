# Password Generator by [Your Name]

import random
import string

print("🔐 Welcome to Your Password Generator")

# Step 1: Ask the user how long they want the password to be
while True:
    try:
        length = int(input("Enter the desired password length (e.g. 8, 12, 16): "))
        if length <= 0:
            print("Please enter a number greater than 0.")
        else:
            break
    except ValueError:
        print("Please enter a valid number.")

# Step 2: Ask if the user wants special characters
use_special = input("Include special characters (like @, #, %, etc.)? (yes/no): ").lower()

# Step 3: Prepare character list
characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
if use_special == "yes":
    characters += string.punctuation  # adds symbols

# Step 4: Generate the password
password = ''.join(random.choice(characters) for _ in range(length))

# Step 5: Show the password to the user
print("\n✅ Your secure password is:")
print(password)

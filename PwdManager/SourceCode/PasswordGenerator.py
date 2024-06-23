import random
import string


class PasswordGenerator:
    def __init__(self, length, use_uppercase, use_numbers, use_symbols):
        self.length = length
        self.use_uppercase = use_uppercase
        self.use_numbers = use_numbers
        self.use_symbols = use_symbols

    def generate_password(self):
        # Start with an empty password
        password = []

        # Define the character sets
        lowercase_letters = string.ascii_lowercase
        uppercase_letters = string.ascii_uppercase
        numbers = string.digits
        symbols = string.punctuation

        # Create a list of the character sets to use
        charsets = [lowercase_letters]
        if self.use_uppercase:
            charsets.append(uppercase_letters)
        if self.use_numbers:
            charsets.append(numbers)
        if self.use_symbols:
            charsets.append(symbols)

        # Generate the password
        for _ in range(self.length):
            # Choose a random character set
            charset = random.choice(charsets)
            # Choose a random character from the set
            char = random.choice(charset)
            # Add the character to the password
            password.append(char)

        # Shuffle the password to ensure randomness
        random.shuffle(password)

        # Convert the list of characters into a string
        password = ''.join(password)

        return password

import subprocess
import sys
import os
from pathlib import Path

# Path expansion for directory: Expanding the tilde '~' to the full path of the user's Desktop/decrypt directory
directory = Path(os.path.expanduser('~/Desktop/decrypt'))

# List all .enc files in the directory: Fetching all files with the '.enc' extension in the specified directory
files = list(directory.glob('*.enc'))

# Color codes for terminal output: Defining color codes for terminal formatting (green, red, reset)
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# Function to attempt decryption using OpenSSL
def decrypt_file(input_file, output_file, password):
    """Attempt to decrypt the file using OpenSSL and the given password."""
    try:
        # Running OpenSSL to decrypt the file with the given password and save it to output_file
        result = subprocess.run(
            ["openssl", "enc", "-d", "-aes-256-cbc", "-in", input_file, "-out", output_file, "-pass", f"pass:{password}"],
            stderr=subprocess.DEVNULL  # Suppressing error messages
        )
        return result.returncode == 0  # Return True if decryption was successful (exit code 0)
    except Exception as e:
        print(f"Error during decryption: {e}")
        return False

# Function to validate if the decrypted file is a valid text file
def validate_decryption(output_file):
    """Check if the decrypted file is a valid text file."""
    try:
        # Running the 'file' command to check the file type of the decrypted file
        result = subprocess.run(
            ["file", output_file],
            capture_output=True,  # Capturing the output
            text=True  # Interpreting the output as text
        )
        return "text" in result.stdout  # If the file is identified as text, return True
    except Exception as e:
        print(f"Error during validation: {e}")
        return False

# Function for manual decryption mode
def main_manual():
    input_file = input("Enter the path to the encrypted file: ")  # User input for encrypted file path
    output_file = "decrypted.txt"  # Output file name for the decrypted content
    password_file = "rockyou.txt"  # Password list file
    password_count = 0  # Initialize password counter outside the loop

    try:
        # Opening the password file and iterating over each password
        with open(password_file, "r") as f:
            for password in f:
                password = password.strip()  # Remove extra whitespace
                password_count += 1  # Increment for each password attempt

                # Attempt decryption with the current password
                if decrypt_file(input_file, output_file, password):
                    # Validate the decrypted file
                    if validate_decryption(output_file):
                        # If successful, print success message and save the password
                        print(f"[ {GREEN}+{RESET} ] File decrypted successfully with password: {password}")
                        print(f"Total attempts: {password_count}")
                        with open("password.txt", "a") as pw_file:
                            pw_file.write(f"Password to {input_file} is: {password}\n")
                        os.system(f"open {output_file}")  # Open the decrypted file (macOS command)
                        return
                    else:
                        # If the decryption is invalid, print error and delete the output file
                        print(f"[ {RED}={RESET} ] Incorrect password: {password}")
                        if os.path.exists(output_file):
                            os.remove(output_file)
                else:
                    # If decryption fails, print error message
                    print(f"[ {RED}-{RESET} ] Failed to decrypt with password: {password}")

        print(f"Decryption failed. No valid password found in {password_file}")

    except FileNotFoundError:
        print(f"Password file {password_file} not found.")  # Handle if the password file is missing
    except Exception as e:
        print(f"An error occurred: {e}")  # Catch any other unexpected errors

# Function for automatic decryption mode (for multiple files)
def main_auto():
    output_file = "decrypted.txt"  # Output file name for decrypted content
    password_file = "rockyou.txt"  # Password list file
    password_count = 0  # Initialize password counter outside the loop

    try:
        # Opening the password file and iterating over each encrypted file
        with open(password_file, "r") as f:
            for input_file in files:
                input_path = str(input_file)  # Convert Path object to string
                print(f"Attempting to decrypt {input_path}...")

                # Iterate over each password in the password file
                for password in f:
                    password = password.strip()  # Remove extra whitespace
                    password_count += 1  # Increment for each password attempt

                    # Attempt decryption with the current password
                    if decrypt_file(input_path, output_file, password):
                        # Validate the decrypted file
                        if validate_decryption(output_file):
                            # If successful, print success message and save the password
                            print(f"[ {GREEN}+{RESET} ] File {input_path} decrypted successfully with password: {password}")
                            print(f"Total attempts: {password_count}")
                            with open("password.txt", "a") as pw_file:
                                pw_file.write(f"Password to {input_path} is: {password}\n")
                            os.system(f"open {output_file}")  # Open the decrypted file (macOS command)
                            return
                        else:
                            # If the decryption is invalid, print error and delete the output file
                            print(f"[ {RED}={RESET} ] Incorrect password: {password}")
                            if os.path.exists(output_file):
                                os.remove(output_file)
                    else:
                        # If decryption fails, print error message
                        print(f"[ {RED}-{RESET} ] Failed to decrypt {input_path} with password: {password}")

        print(f"Decryption failed. No valid password found in {password_file}")

    except FileNotFoundError:
        print(f"Password file {password_file} not found.")  # Handle if the password file is missing
    except Exception as e:
        print(f"An error occurred: {e}")  # Catch any other unexpected errors

# Main entry point of the program
if __name__ == "__main__":
    if len(sys.argv) == 2:  # Check if there is one argument provided
        if sys.argv[1] == "--manual":  # If manual mode is selected
            main_manual()
        elif sys.argv[1] == "--auto":  # If automatic mode is selected
            main_auto()
        elif sys.argv[1] == "--help":  # If help mode is selected
            print("Usage: python decrypt.py [--manual] [--help]")
            print("--manual: Decrypts the file with the given password.")
            print("--auto: Decrypts all .enc files in the specified directory.")
            print("--help: Displays this help message.")
    else:
        print("Invalid arguments. Use --help for usage instructions.")  # Error message for invalid arguments
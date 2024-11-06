import subprocess
import sys
import time
import os
from pathlib import Path

try:
    # Get the directory of the current script
    script_directory = os.path.dirname(__file__)

    # Path expansion for directory: Expanding the tilde '~' to the full path of the user's Desktop/decrypt directory
    files = list(Path(script_directory).glob('*.enc'))  # Correct usage of glob with Path

    # Color codes for terminal output: Defining color codes for terminal formatting (green, red, reset)
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"

    # Initialize the counter to track total password attempts
    password_count = 0

    # Function to attempt decryption using OpenSSL
    def decrypt_file(input_file, output_file, password):
        """Attempt to decrypt the file using OpenSSL and the given password."""
        try:
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
            result = subprocess.run(
                ["file", output_file],
                capture_output=True,
                text=True
            )
            return "text" in result.stdout  # If the file is identified as text, return True
        except Exception as e:
            print(f"Error during validation: {e}")
            return False

    # Function for manual decryption mode
    def main_manual():
        global password_count
        input_file = input("Enter the path to the encrypted file: ")
        output_file = "decrypted.txt"
        password_file = "rockyou.txt"
        if input_file == "":
            print("No file specified. Exiting...")
            sys.exit(1)
        else:

            try:
                with open(password_file, "r") as f:
                    for password in f:
                        password = password.strip()
                        password_count += 1  # Increment for each password attempt

                        if decrypt_file(input_file, output_file, password):
                            if validate_decryption(output_file):
                                print(f"[ {GREEN}+{RESET} ] File decrypted successfully with password: {password}")
                                print(f"Total attempts: {password_count}")
                                with open("password.txt", "a") as pw_file:
                                    pw_file.write(f"Password to {input_file} is: {password}\n")
                                os.system(f"open {output_file}")
                                return
                            else:
                                print(f"[ {RED}={RESET} ] Incorrect password: {password}")
                                if os.path.exists(output_file):
                                    os.remove(output_file)
                        else:
                            print(f"[ {RED}-{RESET} ] Failed to decrypt with password: {password}")

                print(f"Decryption failed. No valid password found in {password_file}")

            except FileNotFoundError:
                print(f"Password file {password_file} not found.")
            except Exception as e:
                print(f"An error occurred: {e}")
        #auto mode
    # Function for automatic decryption mode (for multiple files)
    def main_auto():
        global password_count
        output_file = "decrypted.txt"
        password_file = "rockyou.txt"

        try:
            with open(password_file, "r") as f:
                passwords = f.readlines()

            for input_file in files:
                input_path = str(input_file)
                print(f"Attempting to decrypt {input_path}...")

                for password in passwords:
                    password = password.strip()
                    password_count += 1

                    if decrypt_file(input_path, output_file, password):
                        if validate_decryption(output_file):
                            print(f"[ {GREEN}+{RESET} ] decrypted successfully with password: {password}")
                            print(f"Total attempts: {password_count}")
                            with open("password.txt", "a") as pw_file:
                                pw_file.write(f"Password to {input_path} is: {password}\n")
                            os.system(f"open {output_file}")
                            return
                        else:
                            print(f"[ {RED}-{RESET} ] Incorrect password: {password}")
                            if os.path.exists(output_file):
                                os.remove(output_file)
                    else:
                        print(f"[ {RED}-{RESET} ] Failed to decrypt with password: {password}")

            print(f"Decryption failed. No valid password found in {password_file}")

        except FileNotFoundError:
            print(f"Password file {password_file} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    # Main entry point of the program
    if __name__ == "__main__":
        if len(sys.argv) == 2:
            if sys.argv[1] == "--manual":
                main_manual()
            elif sys.argv[1] == "--auto":
                main_auto()
            elif sys.argv[1] == "--help":
                print("Usage: python decrypt.py [--manual] [--auto] [--help]")
                print("--manual: Decrypts the file with the given password.")
                print("--auto: Decrypts all .enc files in the specified directory.")
                print("--help: Displays this help message.")
        else:
            print("Invalid arguments. Use --help for usage instructions.")

except KeyboardInterrupt:
    print("\nProgram interrupted.")
    print(f"Total password attempts before interruption: {password_count}")
import subprocess
import sys
import time
import os
from pathlib import Path

start_time = time.time()

# Get script directory
script_directory = os.path.dirname(__file__)
files = list(Path(script_directory).glob('*.enc'))

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

password_count = 0

def show_two_decimals(number):
    return "{:.2f}".format(number)

def decrypt_file(input_file, output_file, password):
    """Attempts to decrypt using OpenSSL."""
    try:
        subprocess.run(
            ["openssl", "enc", "-d", "-aes-256-cbc", "-in", input_file, "-out", output_file, "-pass", f"pass:{password}"],
            stderr=subprocess.DEVNULL,
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False

def main_manual():
    global password_count
    input_file = input("Enter the path to the encrypted file: ").strip()
    if not input_file:
        print("No file specified. Exiting...")
        sys.exit(1)

    output_file = "decrypted.txt"
    password_file = "rockyou.txt"

    try:
        with open(password_file, "r") as f:
            passwords = f.read().splitlines()  # Read once, store in memory

        for password in passwords:
            password_count += 1
            if decrypt_file(input_file, output_file, password):
                print(f"[ {GREEN}+{RESET} ] Decrypted with password: {password}")
                print(f"Total attempts: {password_count}")
                with open("password.txt", "a") as pw_file:
                    pw_file.write(f"Password for {input_file}: {password}\n")
                os.system(f"open {output_file}")
                return
            else:
                print(f"[ {RED}-{RESET} ] Failed with password: {password}")

        print(f"Decryption failed. No valid password found in {password_file}")

    except FileNotFoundError:
        print(f"Password file {password_file} not found.")

def main_auto():
    global password_count
    output_file = "decrypted.txt"
    password_file = "rockyou.txt"

    try:
        with open(password_file, "r") as f:
            passwords = f.read().splitlines()

        for input_file in files:
            print(f"Attempting to decrypt {input_file}...")
            for password in passwords:
                password_count += 1
                if decrypt_file(str(input_file), output_file, password):
                    print(f"[ {GREEN}+{RESET} ] Decrypted successfully with password: {password}")
                    print(f"Total attempts: {password_count}")
                    with open("password.txt", "a") as pw_file:
                        pw_file.write(f"Password for {input_file}: {password}\n")
                    os.system(f"open {output_file}")
                    return
                else:
                    print(f"[ {RED}-{RESET} ] Failed with password: {password}")

        print(f"Decryption failed. No valid password found in {password_file}")

    except FileNotFoundError:
        print(f"Password file {password_file} not found.")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "--manual":
            main_manual()
        elif sys.argv[1] == "--auto":
            main_auto()
        else:
            print("Usage: python decrypt.py [--manual] [--auto]")
    else:
        print("Invalid arguments. Use --manual or --auto.")

import subprocess
import os

# Color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def decrypt_file(input_file, output_file, password):
    """Attempt to decrypt the file using OpenSSL and the given password."""
    try:
        result = subprocess.run(
            ["openssl", "enc", "-d", "-aes-256-cbc", "-in", input_file, "-out", output_file, "-pass", f"pass:{password}"],
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error during decryption: {e}")
        return False

def validate_decryption(output_file):
    """Check if the decrypted file is a valid text file."""
    try:
        result = subprocess.run(
            ["file", output_file],
            capture_output=True,
            text=True
        )
        return "text" in result.stdout
    except Exception as e:
        print(f"Error during validation: {e}")
        return False

def main():
    input_file = input("Enter the path to the encrypted file: ")
    output_file = "decrypted.txt"
    password_file = "rockyou.txt"
    password_count = 0  # Initialize password counter outside the loop

    try:
        with open(password_file, "r") as f:
            for password in f:
                password = password.strip()
                password_count += 1  # Increment for each password attempt

                # Attempt decryption
                if decrypt_file(input_file, output_file, password):
                    # Validate the decrypted file
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

if __name__ == "__main__":
    main()
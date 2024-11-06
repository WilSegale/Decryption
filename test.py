import os

# Define colors for output (use appropriate color codes or remove if not needed)
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def decrypt_file(input_file, output_file, password):
    # Placeholder for the decryption logic
    # Return True if the decryption is successful, else False
    pass

def validate_decryption(output_file):
    # Placeholder to validate if the decryption was successful
    # Return True if the file is valid, else False
    pass

def main():
    # Specify the directory to search
    directory = '/Users/zero/Desktop/decrypt'

    # List all files in the directory with .enc extension
    files = [f for f in os.listdir(directory) if f.endswith('.enc')]

    # Initialize password counter outside the loop
    password_file = "rockyou.txt"
    password_count = 0  # Initialize password counter

    for input_file in files:
        input_path = os.path.join(directory, input_file)
        output_file = "decrypted.txt"

        try:
            with open(password_file, "r") as f:
                for password in f:
                    password = password.strip()
                    password_count += 1  # Increment for each password attempt

                    # Attempt decryption
                    if decrypt_file(input_path, output_file, password):
                        # Validate the decrypted file
                        if validate_decryption(output_file):
                            print(f"[ {GREEN}+{RESET} ] File {input_file} decrypted successfully with password: {password}")
                            print(f"Total attempts: {password_count}")
                            with open("password.txt", "a") as pw_file:
                                pw_file.write(f"Password to {input_file} is: {password}\n")
                            os.system(f"open {output_file}")  # Open the decrypted file
                            return
                        else:
                            print(f"[ {RED}={RESET} ] Incorrect password: {password}")
                            if os.path.exists(output_file):
                                os.remove(output_file)
                    else:
                        print(f"[ {RED}-{RESET} ] Failed to decrypt {input_file} with password: {password}")

            print(f"Decryption failed for {input_file}. No valid password found in {password_file}")

        except FileNotFoundError:
            print(f"Password file {password_file} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

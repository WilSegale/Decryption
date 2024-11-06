import subprocess
import getpass
import os
os.system("ls")
def encrypt_file(input_file, output_file, password):
    """Encrypts a file using openssl with aes-256-cbc."""
    command = [
        "openssl", "enc", "-aes-256-cbc", "-salt",
        "-in", input_file, "-out", output_file,
        "-pass", f"pass:{password}"
    ]
    subprocess.run(command, check=True)
    print(f"File encrypted to {output_file}")

def main():
    # Get user input
    input_file = input("Input file name to encrypt: ")
    encrypt_file_name = input("Name the encrypted file (without extension): ")
    output_file = f"{encrypt_file_name}.enc"
    password = getpass.getpass("Input Password: ")

    # Encrypt the file
    encrypt_file(input_file, output_file, password)

if __name__ == "__main__":
    main()

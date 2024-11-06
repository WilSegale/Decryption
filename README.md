# File Decryption Script

This Python script attempts to decrypt an encrypted file using passwords from a password list. The script uses OpenSSL for decryption and verifies if the output is a valid text file. If successful, the password is saved to a `password.txt` file.

## Features
- Attempts to decrypt a file using AES-256-CBC encryption with passwords from a provided password file.
- Validates if the decrypted file is a text file.
- Saves the correct password to a file called `password.txt`.
- Supports using a commonly available password list (like `rockyou.txt`).

## Requirements
- Python 3.x
- OpenSSL
- A password list file (e.g., `rockyou.txt`)
- The `file` command on the system (used for validation)

## Installation

1. Ensure that **OpenSSL** is installed on your system. You can check if OpenSSL is available by running:
   ```bash
   openssl version
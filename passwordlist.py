import random
import string
import time

# Prompt the user for the desired password length
try:
    length = int(input("INPUT THE LENGTH OF THE PASSWORD\n>>> "))
except ValueError:
    print("Invalid input. Please enter a number.")
    exit()
    
def generate_password(length):
    """Generates a random password of a given length."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def main():
    password_count = 0
    start_time = time.time()
    
    # Open the file for writing passwords and ensure it closes properly
    with open('rockyou.txt', 'a') as FilePassword:
        try:
            while True:
                password = generate_password(length)  # Pass `length` here
                password_count += 1
                print(f"Password {password_count}: {password}")
                print(password, file=FilePassword)  # Write to file

                # Optional delay for readability (uncomment if needed)
                # time.sleep(0.5)
            
        except KeyboardInterrupt:
            print("\nPassword generation stopped.")
            print(f"Total passwords generated: {password_count}")
            total_time = time.time() - start_time
            print(f"Total time elapsed: {total_time:.2f} seconds")

if __name__ == "__main__":
    main()
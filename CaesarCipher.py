# Get inputs
original_message = input("Enter the message you want to encrypt: ")
shift = int(input("Enter the shift value: (e.g :3)"))

def caesar_cipher_encrypt(message, shift):
    encrypted = []
    for char in message:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            encrypted.append(chr((ord(char) - shift_base + shift) % 26 + shift_base))
        elif char.isdigit():  # Check if the character is a digit
            encrypted.append(chr((ord(char) - ord('0') + shift) % 10 + ord('0')))
        else:
            encrypted.append(char)  # Non-alphabetic and non-numeric characters remain unchanged
    return ''.join(encrypted)

def caesar_cipher_decrypt(encrypted_message, shift):
    return caesar_cipher_encrypt(encrypted_message, -shift)

# Encrypt the message
encrypted_message = caesar_cipher_encrypt(original_message, shift)
print(f"Encrypted message: {encrypted_message}")

# Decrypt the message
decrypted_message = caesar_cipher_decrypt(encrypted_message, shift)
print(f"Decrypted message: {decrypted_message} Shift Value:{shift}")


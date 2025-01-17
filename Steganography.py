# StegEM Python module for visual steganography created to hide and obfuscate information within an image

# WELCOME MESSAGE
print(
    "Welcome to StegEM! Please note that this tool should only be used for ethical purposes and never with bad intent. "
    "You are responsible for your own actions, and no one else but you is at fault for what happens with the modified files/imagery. Thank you!"
)
print()

# Imports
import os
from PIL import Image
import random
import string

# Helper Functions
def create_directory(path):
    """Create a directory if it doesn't exist."""
    try:
        os.makedirs(path, exist_ok=True)
        print(f"Directory created or already exists: {path}")
        return path
    except Exception as e:
        print(f"Error creating directory: {e}")
        exit()
def calculate_max_message_size(image):
    """Calculate the maximum size of data that can be embedded into the image."""
    width, height = image.size
    max_bits = width * height * 3  # Each pixel can store 3 bits (one per color channel)
    max_characters = max_bits // 8  # Convert bits to characters (1 byte = 8 bits)
    return max_characters

def generate_random_delimiter(length=32):
    """Generate a random delimiter with a specified length."""
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))

def get_delimiter():
    """Ask the user if they want to use a custom delimiter or the default one."""
    choice = input("Would you like to use a custom delimiter? (Y/N): ").strip().upper()
    if choice == 'Y':
        print("Please note that the delimiter should be unique and must be in 0 and 1 in binary!")
        custom_delimiter = input("Please enter your custom delimiter: ").strip()
        # Validate that the delimiter is non-empty and unique
        if not all(bit in ['0', '1'] for bit in custom_delimiter) or len(custom_delimiter) < 15:
            print("Delimiter must consist only of '0' and '1' and be at least 15 characters long... Falling back to a default delimiter.")
            return generate_random_delimiter()
        else:
            return custom_delimiter
    elif choice == 'N':
        # Use a long, hardcoded default delimiter
        return '00001111000011110000111100001111'  # Example of a long, unlikely sequence
    else:
        print("Invalid choice! Falling back to default delimiter.")
        return generate_random_delimiter()  # Fallback to random if input is unclear

def embed_message(image, delimiter):
    """Embed a message into an image using LSB."""
    # Calculate max message size
    max_message_size = calculate_max_message_size(image)
    print(f"The maximum size of the message you can embed is {max_message_size} characters.")

    # Ask for the message
    message = input("Please enter the message to embed: ")

    if len(message) > max_message_size:
        print("Warning: The message is too long and will cause significant image degradation. Consider shortening it.")
        confirmation = input("Do you still want to proceed with embedding this message? (Y/N): ").strip().upper()
        if confirmation != "Y":
            print("Aborting embedding process.")
            return
    else:
        print("Message size is acceptable. Proceeding with embedding...")

    # Convert the message to binary and append a delimiter
    binary_message = ''.join(format(ord(char), '08b') for char in message) + delimiter
    binary_index = 0

    # Ensure image is in RGB mode
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Access pixel data
    pixels = image.load()
    width, height = image.size

    # Modify pixels with the binary message
    for y in range(height):
        for x in range(width):
            if binary_index < len(binary_message):
                r, g, b = pixels[x, y]

                # Modify the least significant bit of the red channel
                r = (r & ~1) | int(binary_message[binary_index])
                binary_index += 1

                # Modify the green channel if needed
                if binary_index < len(binary_message):
                    g = (g & ~1) | int(binary_message[binary_index])
                    binary_index += 1

                # Modify the blue channel if needed
                if binary_index < len(binary_message):
                    b = (b & ~1) | int(binary_message[binary_index])
                    binary_index += 1

                # Update the pixel
                pixels[x, y] = (r, g, b)

    # Save the modified image
    output_path = os.path.join(path_to_destination_folder, "embedded_image.png")
    image.save(output_path)
    print(f"Message successfully embedded! Modified image saved at: {output_path}")

def retrieve_message(image, delimiter):
    """Retrieve a hidden message from an image using LSB."""
    print("Retrieving the message...")

    # Ensure the image is in RGB mode
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Access pixel data
    pixels = image.load()
    width, height = image.size

    binary_message = ""

    # Read the least significant bits from the pixel data
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            # Extract the LSB from the red channel
            binary_message += str(r & 1)
            if delimiter in binary_message:
                break

            # Extract the LSB from the green channel
            binary_message += str(g & 1)
            if delimiter in binary_message:
                break

            # Extract the LSB from the blue channel
            binary_message += str(b & 1)
            if delimiter in binary_message:
                break
        if delimiter in binary_message:
            break

    # Remove the delimiter and convert binary to the message
    if delimiter in binary_message:
        binary_message = binary_message[:binary_message.find(delimiter)]
        message = ''.join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8))
        print(f"Retrieved message: {message}")
    else:
        print("No hidden message found or the image might not contain a valid embedded message.")

def validate_image_format(image_path):
    """Validate the image format and warn the user about lossy formats."""
    try:
        with Image.open(image_path) as img:
            if img.format not in ['PNG', 'BMP']:
                print(f"Warning: The image is in a lossy format ({img.format}). This may lead to corrupted data or message. Proceed with caution.")
            print(f"Image format validated: {img.format}")
    except Exception as e:
        print(f"Error validating the image format: {e}")
        exit()


# Step 1: User Input
path_to_original_image = input("Please input the PATH to the image you want to modify: ")

# Validate image format
validate_image_format(path_to_original_image)

ask_path_to_destination_folder = input(
    "Do you have a PATH to the directory you want to store the modified image? (Y/N): ").strip().capitalize()

if ask_path_to_destination_folder == "Y":
    path_to_destination_folder = input("Please provide the PATH to the destination folder: ").strip()
    create_directory(path_to_destination_folder)
elif ask_path_to_destination_folder == "N":
    print("Automatically generating a directory for the result image destination...")
    path_to_destination_folder = create_directory("Modified_Images_StegEM")
else:
    print("Invalid option. Exiting.")
    exit()

# Step 2: Load Image
try:
    image = Image.open(path_to_original_image)
    print(f"Image successfully loaded: {path_to_original_image}")
    print(f"Image size: {image.size}, Mode: {image.mode}")
except Exception as e:
    print(f"Error loading the image: {e}")
    exit()

# Step 3: Get the delimiter
delimiter = get_delimiter()

# Step 4: Next Steps
action = input("Would you like to (E) Embed a message or (R) Retrieve a message  (C)Caesar Cipher Message or (W) Add a Watermark? ").strip().upper()

if action == 'E':
    embed_message(image, delimiter)
elif action == 'R':
    retrieve_message(image, delimiter)
elif action == "W":
    # Import the watermarking function here to avoid circular imports at the top
    from Watermarking import user_driven_watermarking
    user_driven_watermarking(path_to_original_image, path_to_destination_folder)
elif action == "C":
    from CaesarCipher import caesar_cipher_encrypt, caesar_cipher_decrypt
    cipher_action = input("Would you like to (E) Encrypt or (D) Decrypt a message? ").strip().upper()
    if cipher_action == "E":
        original_message = input("Enter the message you want to encrypt: ")
        shift = int(input("Enter the shift value (e.g., 3): "))
        encrypted_message = caesar_cipher_encrypt(original_message, shift)
        print(f"Encrypted message: {encrypted_message}")
    elif cipher_action == "D":
        encrypted_message = input("Enter the encrypted message you want to decrypt: ")
        shift = int(input("Enter the shift value (e.g., 3): "))
        decrypted_message = caesar_cipher_decrypt(encrypted_message, shift)
        print(f"Decrypted message: {decrypted_message}")
    else:
        print("Invalid option selected. Returning to main menu.")
else:
    print("Invalid option selected. Exiting.")

# Step 6: Delete the original image...
def delete_original_image(path_to_original_image):
    permission_delete_original = input("Do you want to delete the original image? Y/N: ").strip().upper()
    if permission_delete_original == "Y":
        try:
            os.remove(path_to_original_image)
            print(f"Original image {path_to_original_image} deleted successfully.")
        except Exception as e:
            print(f"Error deleting the original image: {e}")
    elif permission_delete_original == "N":
        print("Original image won't be deleted.")
    else:
        print("Invalid input! Please respond with Y or N.")

delete_original_image(path_to_original_image)

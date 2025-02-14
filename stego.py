from PIL import Image
import numpy as np
from crypto import encrypt_message, decrypt_message

def hide_message(image_path, message, password, output_path):
    # Encrypt the message
    encrypted_data = encrypt_message(message, password)
    
    # Convert encrypted data to binary
    binary_message = ''.join(format(byte, '08b') for byte in encrypted_data)
    binary_message += '1111111111111110'  # Delimiter
    
    # Open image and hide message
    img = Image.open(image_path)
    img_array = np.array(img)
    
    # Check if message fits
    max_bits = img_array.size * 3
    if len(binary_message) > max_bits:
        raise ValueError("Message too long!")
    
    # Hide message in LSB
    data_index = 0
    for pixel in np.nditer(img_array, op_flags=['readwrite']):
        if data_index < len(binary_message):
            pixel[...] = (pixel & 0b11111110) | int(binary_message[data_index])
            data_index += 1
    
    # Save the stego image
    Image.fromarray(img_array).save(output_path)
    print("Message hidden!")

def extract_message(image_path, password):
    # Extract binary message
    img = Image.open(image_path)
    img_array = np.array(img)
    
    binary_message = []
    for pixel in np.nditer(img_array):
        binary_message.append(str(pixel & 1))
    
    binary_str = ''.join(binary_message)
    delimiter = '1111111111111110'
    end_index = binary_str.find(delimiter)
    
    if end_index == -1:
        return "No message found!"
    
    encrypted_data = bytes(int(binary_str[i:i+8], 2) for i in range(0, end_index, 8))
    return decrypt_message(encrypted_data, password)
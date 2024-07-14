from PIL import Image
import os
from cryptography.fernet import Fernet
import base64

def generate_key():
    key = Fernet.generate_key()
    with open('key.key', 'wb') as key_file:
        key_file.write(key)
    return key

def load_key():
    return open('key.key', 'rb').read()

def encrypt_message(message, key):
    cipher = Fernet(key)
    return cipher.encrypt(message.encode())

def decrypt_message(encrypted_message, key):
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_message).decode()

def message_to_bits(message):
    return ''.join(format(ord(char), '08b') for char in message)

def embed_message(image_path, message, output_path):
    image = Image.open(image_path)
    image = image.convert('RGB')
    pixels = list(image.getdata())

    message_bits = message_to_bits(message)
    message_length = len(message_bits)
    data_index = 0

    new_pixels = []

    for pixel in pixels:
        
        #set lsb of r field to zero, and then assign it to the message_bits at index
        r, g, b = pixel

        if data_index < message_length:
            r = (r & 0xFE) | int(message_bits[data_index])
            data_index += 1 
        if data_index < message_length:
            g = (g & 0xFE) | int(message_bits[data_index])
            data_index += 1
        if data_index < message_length:
            b = (b & 0xFE) | int(message_bits[data_index])
            data_index += 1

        new_pixels.append((r, g, b))

    image.putdata(new_pixels)
    image.save(output_path)
    print('Message embedded and image saved.')


def extract_message(image_path, key):
    image = Image.open(image_path)
    image = image.convert('RGB')
    pixels = list(image.getdata())

    binary_message = ''
    for pixel in pixels:
        r, g, b = pixel
        binary_message += str(r & 1)
        binary_message += str(g & 1)
        binary_message += str(b & 1)

    #split the binary string into 8 bit chunks
    message_bits = [binary_message[i: i + 8] for i in range(0, len(binary_message), 8)]
    #convert 8 bit to int, convert that to ASCII, filter out null chars, join into a string
    message = ''.join([chr(int(bits, 2)) for bits in message_bits if int(bits, 2) != 0])

    while len(message) % 4 != 0:
        message += '='

    encrypted_message = base64.urlsafe_b64decode(message.encode())
    return decrypt_message(encrypted_message, key)



def main():
    if not os.path.exists('key.key'):
        key = generate_key()
    else:
        key = load_key()

    message = 'The british are coming, the british are coming!'
    encrypted_message = encrypt_message(message, key)
    encrypted_message_b64 = base64.urlsafe_b64encode(encrypted_message).decode()

    image_path = 'flowers.png'
    output_image_path = 'encrypted_flowers.png'

    embed_message(image_path, encrypted_message_b64, output_image_path)

    decrypted_message = extract_message(output_image_path, key)
    print("decrypted message: ", decrypted_message)


if __name__ == '__main__':
    main()



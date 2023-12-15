import os
import zipfile
from PIL import Image
from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

key = get_random_bytes(16)

# Function to compress image files
def compress_image(image_path, output_path, quality):
    """
    Compress an image, retaining its original dimensions for the learning mode
    but reducing file size on disk.
    :param image_path: Path to the original image.
    :param output_path: Path to save the compressed image.
    :param quality: Quality level for compression, between 1 (worst) and 95 (best). 85 is recommended.
    """
    with Image.open(image_path) as img:
        img.save(output_path, 'JPEG', optimize=True, quality=quality)  

# Function to zip image files
def zip_files(source_folder, output_zip):
    print("Compressing files")
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_folder):
            for file in files:
                if file.endswith('.jpeg'):
                    full_path = os.path.join(root, file)
                    # Compress and save the image temporarily
                    compressed_image_path = full_path + '.compressed.jpeg'
                    compress_image(full_path, compressed_image_path, quality=50)
                    # Add the compressed image to the zip
                    zipf.write(compressed_image_path, os.path.relpath(compressed_image_path, source_folder))
                    # Remove the temporary compressed image
                    os.remove(compressed_image_path)

# Function to encrypt image files
def encrypt_image(input_file, output_file, key):
    print("Encrypting files")
    cipher = AES.new(key, AES.MODE_CBC)
    with open(input_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            f_out.write(cipher.iv)
            data = f_in.read()
            f_out.write(cipher.encrypt(pad(data, AES.block_size)))

# Function to decrypt image files
def decrypt_image(input_file, output_file, key):
    print("Decrypting files")
    with open(input_file, 'rb') as f_in:
        iv = f_in.read(16)  # AES block size is 16 bytes
        cipher = AES.new(key, AES.MODE_CBC, iv)
        with open(output_file, 'wb') as f_out:
            data = f_in.read()
            f_out.write(unpad(cipher.decrypt(data), AES.block_size))

# Function to unzip image files
def unzip_files(input_zip, output_folder):
    print("Decompressing files")
    with zipfile.ZipFile(input_zip, 'r') as zip_ref:
        zip_ref.extractall(output_folder)

# Encrypt and compress images
def encrypt_files(root_dir):
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.jpeg'):
                image_path = os.path.join(root, file)
                zip_files(root, image_path + '.zip')  # Compress the entire directory
                encrypt_image(image_path + '.zip', image_path + '.enc', key)
                os.remove(image_path + '.zip')  # Remove the zip file after encryption

# Decrypt and decompress images
def decrypt_files(root_dir):
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.enc'):
                image_path = os.path.join(root, file)
                base_image_path = image_path.rsplit('.enc', 1)[0]
                decrypt_image(image_path, base_image_path + '.zip', key)
                unzip_files(base_image_path + '.zip', root)  # Decompress in the same directory
                os.remove(base_image_path + '.zip')  # Remove the zip file after decompression
                os.remove(image_path)  # Remove the encrypted file

encrypt_files('chest_xray')
decrypt_files('chest_xray')
"""
This script provides functions to encrypt and decrypt strings using DES encryption.

kld.sjtu.edu.cn uses DES encryption to secure the data transmission between the client and the server.
It follows the following steps:
1. Convert the plaintext string to GBK-encoded bytes.
2. Pad the data to match the DES block size.
3. Encrypt the data using DES in CBC mode.
4. Perform Base64 encoding and then URL encoding.
5. Perform URL encoding for data transmission.
"""

import json
import base64
from urllib.parse import unquote, quote
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

# Define DES key (8 bytes) and IV (initialization vector)
DES_KEY = b"85281581"  # DES key must be 8 bytes long
IV = b"univlive"  # IV must also be 8 bytes long

def des_encrypt(text: str) -> str:
    """
    Encrypts a string using DES in CBC mode, then encodes
    it in Base64 and URL encoding.
    
    Parameters
    ----------
    text : str
        The plaintext string to encrypt.
    
    Returns
    -------
    encrypted_string : str
        The encrypted string (Base64 + URL encoded).
    """
    # Convert the string to GBK-encoded bytes
    data = text.encode("gbk")
    
    # Pad data to match DES block size
    padded_data = pad(data, DES.block_size)
    
    # Create DES encryption object
    cipher = DES.new(DES_KEY, DES.MODE_CBC, IV)
    encrypted_data = cipher.encrypt(padded_data)
    
    # Perform Base64 encoding and then URL encoding
    encrypted_string = quote(base64.b64encode(encrypted_data))
    return encrypted_string

def encrypt(data: dict[str, str]) -> str:
    """
    Encrypts a dictionary as a JSON string using DES encryption
    and formats it as an order request body.
    
    Parameters
    ----------
    data : dict[str, str]
        The dictionary to encrypt.

    Returns
    -------
    body : str
        The encrypted order request body.
    """
    json_data = json.dumps(data, separators=(',', ':'))
    order = des_encrypt(json_data)
    return f"order={order}"

def decrypt(encrypted_text: str) -> str:
    """
    Decrypts a DES CBC-encrypted string.
    
    Parameters
    ----------
    encrypted_text : str
        The encrypted string to decrypt.

    Returns
    -------
    decrypted_string : str
        The decrypted plaintext
    """
    # Perform URL decoding first
    decoded_text = unquote(encrypted_text)
    
    # Perform Base64 decoding
    encrypted_data = base64.b64decode(decoded_text)
    
    # Create DES decryption object
    cipher = DES.new(DES_KEY, DES.MODE_CBC, IV)
    decrypted_data = cipher.decrypt(encrypted_data)
    
    # Remove padding and decode as GBK string
    decrypted_string = unpad(decrypted_data, DES.block_size).decode("gbk")
    return decrypted_string



if __name__ == "__main__":
    # Test cases
    original_text = "Hello, DES!"
    encrypted_text = des_encrypt(original_text)
    decrypted_text = decrypt(encrypted_text)
    
    print(f"Original Text: {original_text}")
    print(f"Encrypted Text: {encrypted_text}")
    print(f"Decrypted Text: {decrypted_text}")
    
    # Ensure correctness
    assert original_text == decrypted_text, "Decryption failed!"

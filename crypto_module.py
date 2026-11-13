import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# ==========================================
# DERIVE AES KEY FROM PASSWORD
# ==========================================

def derive_key(password, salt):

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600_000
    )

    return kdf.derive(password.encode("utf-8"))


# ==========================================
# ENCRYPT FILE
# ==========================================

def encrypt_file(input_file, output_file, password):

    # Generate random salt and nonce
    salt = os.urandom(16)
    nonce = os.urandom(12)

    # Read original file
    with open(input_file, "rb") as file:
        data = file.read()

    # Generate AES-256 key
    key = derive_key(password, salt)

    # AES-256-GCM encryption
    aesgcm = AESGCM(key)

    encrypted_data = aesgcm.encrypt(
        nonce,
        data,
        None
    )

    # Store:
    # SALT + NONCE + ENCRYPTED DATA
    with open(output_file, "wb") as file:
        file.write(salt)
        file.write(nonce)
        file.write(encrypted_data)


# ==========================================
# DECRYPT FILE
# ==========================================

def decrypt_file(input_file, output_file, password):

    try:

        # Read encrypted file
        with open(input_file, "rb") as file:
            encrypted_data = file.read()

        # Extract salt
        salt = encrypted_data[:16]

        # Extract nonce
        nonce = encrypted_data[16:28]

        # Extract ciphertext
        ciphertext = encrypted_data[28:]

        # Generate same AES key
        key = derive_key(password, salt)

        # AES-GCM decryption
        aesgcm = AESGCM(key)

        decrypted_data = aesgcm.decrypt(
            nonce,
            ciphertext,
            None
        )

        # Write recovered file
        with open(output_file, "wb") as file:
            file.write(decrypted_data)

        return True

    except Exception:
        return False
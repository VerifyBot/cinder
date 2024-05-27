import random


class DiffieHellman:
    """
    A class implementing the Diffie-Hellman key exchange protocol.
    """

    P = 9_007_199_254_740_881  # A large prime number
    G = 2  # Generator

    @staticmethod
    def generate_public_key(private_key: int) -> int:
        """
        Generates a public key based on the provided private key.

        Args:
        - private_key (int): The private key.

        Returns:
        - int: The public key.
        """
        # G^private_key % P
        return pow(DiffieHellman.G, private_key, DiffieHellman.P)

    @staticmethod
    def generate_shared_key(other_public_key: int, private_key: int) -> int:
        """
        Generates a shared key based on the provided other party's public key and own private key.

        Args:
        - other_public_key (int): The other party's public key.
        - private_key (int): Own private key.

        Returns:
        - int: The shared key.
        """
        # other_public_key^private_key % P
        return pow(other_public_key, private_key, DiffieHellman.P)

    @staticmethod
    def generate_private_key(min: int = 10, max: int = 20) -> int:
        """
        Generates a random private key within a specific range.

        Returns:
        - int: The generated private key.
        """
        return random.randint(min, max)

    @staticmethod
    def get_public_params() -> dict[str, int]:
        """
        Returns public parameters (G and P) used in the Diffie-Hellman key exchange.

        Returns:
        - dict[str, int]: A dictionary containing 'g' (generator) and 'p' (prime modulus).
        """
        return {"g": DiffieHellman.G, "p": DiffieHellman.P}


from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import hashlib


class AES:
    """
    A class providing AES encryption and decryption functionalities.
    """

    @staticmethod
    def encrypt(message: str, key: str) -> str:
        """
        Encrypts a message using AES encryption.

        Args:
        - message (str): The message to encrypt.
        - key (str): The encryption key.

        Returns:
        - str: The hexadecimal representation of the encrypted ciphertext.
        """

        # Pad the message to be a multiple of 16 bytes (AES block size)
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(message.encode())
        padded_data += padder.finalize()

        # Create an AES cipher object
        cipher = Cipher(
            algorithms.AES(bytes.fromhex(key)),
            modes.ECB(),
            backend=default_backend(),
        )

        # Encrypt the message
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return ciphertext.hex()

    @staticmethod
    def decrypt(ciphertext: str, key: str) -> str:
        """
        Decrypts a ciphertext using AES decryption.

        Args:
        - ciphertext (str): The hexadecimal representation of the ciphertext.
        - key (str): The decryption key.

        Returns:
        - str: The decrypted message.
        """

        if isinstance(ciphertext, dict):  # empty data
            return '{}'

        # Create an AES cipher object
        cipher = Cipher(
            algorithms.AES(bytes.fromhex(key)),
            modes.ECB(),
            backend=default_backend(),
        )

        # Decrypt the ciphertext
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(bytes.fromhex(ciphertext)) + decryptor.finalize()

        try:
            # Unpad the decrypted data
            unpadder = padding.PKCS7(128).unpadder()
            data = unpadder.update(padded_data)
            data += unpadder.finalize()
        except ValueError:
            # If unpadding fails, return the unpadded data directly
            return padded_data.decode("utf-8")

        return data.decode("utf-8")

    @staticmethod
    def diffie_hellman_key_to_aes_key(diffie_hellman_key: int) -> str:
        """
        Converts a Diffie-Hellman key to an AES key using SHA-256 hashing.

        Args:
        - diffie_hellman_key (int): The Diffie-Hellman key.

        Returns:
        - str: The AES key obtained from the Diffie-Hellman key.
        """
        return hashlib.sha256(str(diffie_hellman_key).encode()).hexdigest()

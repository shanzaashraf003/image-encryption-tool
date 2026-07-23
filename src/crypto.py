"""
crypto.py

Provides XOR-based encryption and decryption for image files.
Uses a pseudo-random keystream generated from the encryption key
to turn encrypted images into complete static noise.
"""

import hashlib
from pathlib import Path
from PIL import Image


class XOREncryption:
    """Handles XOR encryption and decryption."""

    @staticmethod
    def _generate_keystream(key: str, length: int) -> bytes:
        """
        Generates a pseudo-random stream of bytes derived from the key
        so short keys produce proper static noise instead of simple color shifts.
        """
        keystream = bytearray()
        counter = 0
        key_bytes = key.encode("utf-8")

        while len(keystream) < length:
            # Hash key + counter to get 32 pseudo-random bytes per iteration
            hasher = hashlib.sha256()
            hasher.update(key_bytes)
            hasher.update(counter.to_bytes(4, byteorder="big"))
            keystream.extend(hasher.digest())
            counter += 1

        return bytes(keystream[:length])

    @staticmethod
    def process(
        input_path: Path,
        output_path: Path,
        key: str,
    ) -> None:
        """
        Encrypts or decrypts an image using XOR operations.
        """
        if not input_path.exists():
            raise FileNotFoundError(f"Input image not found:\n{input_path}")

        if not key.strip():
            raise ValueError("Encryption key cannot be empty.")

        # Open image and ensure RGB mode
        with Image.open(input_path) as img:
            image = img.convert("RGB")
            width, height = image.size
            pixels = image.load()

            total_bytes = width * height * 3
            keystream = XOREncryption._generate_keystream(key, total_bytes)

            key_index = 0
            for y in range(height):
                for x in range(width):
                    red, green, blue = pixels[x, y]

                    red ^= keystream[key_index]
                    green ^= keystream[key_index + 1]
                    blue ^= keystream[key_index + 2]
                    key_index += 3

                    pixels[x, y] = (red, green, blue)

            # Always save as PNG to maintain exact pixel bit values
            image.save(output_path, format="PNG")
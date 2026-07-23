"""
file_handler.py

Handles image validation, preview loading, and output file generation.
"""

from pathlib import Path
from PIL import Image


class FileHandler:
    """Utility methods for image handling."""

    SUPPORTED_EXTENSIONS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".gif",
        ".tiff",
        ".webp",
    }

    OUTPUT_DIRECTORY = Path("output")

    @classmethod
    def ensure_output_directory(cls) -> Path:
        """Creates output directory if it does not already exist."""
        cls.OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
        return cls.OUTPUT_DIRECTORY

    @classmethod
    def validate_image(cls, image_path: Path) -> None:
        """Validates an image file."""
        if not image_path.exists():
            raise FileNotFoundError("Selected image does not exist.")

        if image_path.suffix.lower() not in cls.SUPPORTED_EXTENSIONS:
            raise ValueError("Unsupported image format.")

        try:
            with Image.open(image_path) as image:
                image.verify()
        except Exception as exc:
            raise ValueError("Invalid or corrupted image file.") from exc

    @classmethod
    def generate_output_path(cls, image_path: Path, operation: str) -> Path:
        """
        Generates output filename and prevents trailing '_encrypted_decrypted' string bugs.
        Always outputs as .png to retain exact XOR bits.
        """
        cls.ensure_output_directory()

        # Clean filename stems (e.g., 'flower_encrypted' -> 'flower')
        base_stem = image_path.stem
        if base_stem.endswith("_encrypted"):
            base_stem = base_stem[:-10]
        elif base_stem.endswith("_decrypted"):
            base_stem = base_stem[:-10]

        filename = f"{base_stem}_{operation}.png"
        return cls.OUTPUT_DIRECTORY / filename
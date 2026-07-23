"""
main.py

Application entry point for Image Encryption Tool.
"""

from gui import ImageEncryptionApp


def main():
    """Starts the application."""
    app = ImageEncryptionApp()
    app.mainloop()


if __name__ == "__main__":
    main()
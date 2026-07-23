"""
gui.py

Modern GUI for the Image Encryption Tool.
"""

from pathlib import Path
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
from customtkinter import CTkImage

from crypto import XOREncryption
from file_handler import FileHandler


class ImageEncryptionApp(ctk.CTk):
    """Main application window."""

    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 700
    PREVIEW_SIZE = (350, 250)

    def __init__(self):
        super().__init__()

        # Window Setup
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.title("Image Encryption Tool")
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.minsize(850, 650)

        # State Variables
        self.selected_image: Path | None = None
        self.current_theme = "Dark"

        # Main Layout Frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="🖼️ Image Encryption Tool",
            font=ctk.CTkFont(size=28, weight="bold"),
        )
        self.title_label.pack(pady=(20, 5))

        self.subtitle = ctk.CTkLabel(
            self.main_frame,
            text="Encrypt and decrypt images using bitwise XOR operations.",
            font=ctk.CTkFont(size=14),
        )
        self.subtitle.pack(pady=(0, 15))

        # Preview Area
        self.preview_frame = ctk.CTkFrame(
            self.main_frame,
            width=380,
            height=280,
            corner_radius=12,
        )
        self.preview_frame.pack(padx=20, pady=10)
        self.preview_frame.pack_propagate(False)

        self.preview_label = ctk.CTkLabel(
            self.preview_frame,
            text="No Image Selected",
            font=ctk.CTkFont(size=16),
        )
        self.preview_label.pack(expand=True)

        # File Chooser
        self.browse_button = ctk.CTkButton(
            self.main_frame,
            text="Browse Image",
            width=200,
            height=42,
            corner_radius=10,
            command=self.browse_image,
        )
        self.browse_button.pack(pady=(15, 15))

        # Password / Key Input
        self.key_entry = ctk.CTkEntry(
            self.main_frame,
            width=350,
            height=40,
            placeholder_text="Enter Secret Key",
            show="•",
        )
        self.key_entry.pack(pady=(0, 15))

        # Operation Buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(pady=5)

        self.encrypt_button = ctk.CTkButton(
            self.button_frame,
            text="Encrypt Image",
            width=170,
            height=42,
            corner_radius=10,
            command=self.encrypt_image,
        )
        self.encrypt_button.grid(row=0, column=0, padx=10)

        self.decrypt_button = ctk.CTkButton(
            self.button_frame,
            text="Decrypt Image",
            width=170,
            height=42,
            corner_radius=10,
            command=self.decrypt_image,
        )
        self.decrypt_button.grid(row=0, column=1, padx=10)

        # Progress & Feedback
        self.progress = ctk.CTkProgressBar(self.main_frame, width=450)
        self.progress.pack(pady=(20, 10))
        self.progress.set(0)

        self.theme_button = ctk.CTkButton(
            self.main_frame,
            text="Switch to Light Mode",
            width=220,
            height=36,
            corner_radius=10,
            command=self.toggle_theme,
        )
        self.theme_button.pack(pady=5)

        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Ready",
            anchor="w",
            font=ctk.CTkFont(size=13),
        )
        self.status_label.pack(fill="x", padx=20, pady=(10, 10))

    # =====================================================
    # GUI Helpers
    # =====================================================

    def update_status(self, message: str) -> None:
        self.status_label.configure(text=message)
        self.update_idletasks()

    def set_progress(self, value: float) -> None:
        self.progress.set(value)
        self.update_idletasks()

    def toggle_theme(self):
        if self.current_theme == "Dark":
            ctk.set_appearance_mode("Light")
            self.current_theme = "Light"
            self.theme_button.configure(text="Switch to Dark Mode")
            self.update_status("Light mode enabled.")
        else:
            ctk.set_appearance_mode("Dark")
            self.current_theme = "Dark"
            self.theme_button.configure(text="Switch to Light Mode")
            self.update_status("Dark mode enabled.")

    # =====================================================
    # Image Operations & Events
    # =====================================================

    def browse_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Supported Images", "*.png *.jpg *.jpeg *.bmp *.webp *.gif *.tiff"),
                ("All Files", "*.*"),
            ],
        )

        if not file_path:
            return

        try:
            image_path = Path(file_path)
            FileHandler.validate_image(image_path)
            self.selected_image = image_path
            self.show_preview()
            self.update_status(f"Selected: {image_path.name}")
        except Exception as error:
            messagebox.showerror("Invalid Image", str(error))

    def show_preview(self):
        if not self.selected_image:
            return

        try:
            with Image.open(self.selected_image) as img:
                image = img.copy()

            image.thumbnail(self.PREVIEW_SIZE)
            preview = CTkImage(
                light_image=image,
                dark_image=image,
                size=image.size,
            )

            self.preview_label.configure(image=preview, text="")
            self.preview_label.image = preview
        except Exception as error:
            messagebox.showerror("Preview Error", str(error))

    def encrypt_image(self):
        self.process_image(operation="encrypted")

    def decrypt_image(self):
        self.process_image(operation="decrypted")

    def process_image(self, operation: str):
        if not self.selected_image:
            messagebox.showwarning("No Image", "Please select an image first.")
            return

        key = self.key_entry.get()
        if not key.strip():
            messagebox.showwarning("Missing Key", "Please enter an encryption key.")
            return

        try:
            self.set_progress(0.2)
            self.update_status(f"{operation.capitalize()}ing image...")

            output_path = FileHandler.generate_output_path(
                self.selected_image, operation
            )

            self.set_progress(0.5)

            XOREncryption.process(
                input_path=self.selected_image,
                output_path=output_path,
                key=key,
            )

            # Auto-select newly saved output image
            self.selected_image = output_path
            self.show_preview()

            self.set_progress(1.0)
            self.update_status(f"Saved: {output_path.name}")

            messagebox.showinfo(
                "Success",
                f"Operation completed successfully!\n\nSaved at:\n{output_path}",
            )

        except Exception as error:
            self.set_progress(0)
            messagebox.showerror("Operation Failed", str(error))
            self.update_status("Operation failed.")
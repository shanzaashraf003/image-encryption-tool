# 🔐 Image Encryption Tool

A modern desktop application built with **Python**, **CustomTkinter**, and **Pillow** that provides **secure, lossless image encryption and decryption** using a **SHA-256-derived XOR keystream**. The application ensures that encrypted images remain valid image files while allowing perfect reconstruction of the original image when decrypted with the correct password.

---

## 📸 Demo

| Original Image | Encrypted Image |
|:---------------:|:---------------:|
| ![Original Image](assets/flower_decrypted.png) | ![Encrypted Image](assets/flower_encrypted.png) |

> The encrypted image appears as random static noise, making the original content completely unreadable without the correct encryption key.

---

# ✨ Features

- **🔒 Lossless XOR Encryption**
  - Encrypts raw RGB pixel data while preserving every pixel value, ensuring no information is lost during encryption or decryption.

- **🔑 SHA-256 Derived Keystream**
  - Uses SHA-256 to expand user passwords into a secure pseudo-random byte stream, preventing predictable encryption patterns.

- **🖼️ Automatic PNG Output**
  - Encrypted images are automatically saved in PNG format to avoid lossy JPEG compression, which could corrupt encrypted pixel data.

- **💻 Modern Graphical User Interface**
  - Built using **CustomTkinter** with a clean and responsive interface featuring:
    - Dark/Light mode
    - Image preview
    - Progress tracking
    - Simple encryption/decryption workflow

---

# 🛠️ Technologies Used

- Python 3
- CustomTkinter
- Pillow (PIL)
- hashlib (SHA-256)

---

# 📁 Project Structure

```text
image-encryption-tool/
│
├── output/                  # Stores encrypted and decrypted images
│
├── src/
│   ├── crypto.py            # XOR encryption/decryption and SHA-256 keystream generation
│   ├── file_handler.py      # File validation and output path management
│   ├── gui.py               # CustomTkinter graphical interface
│   └── main.py              # Application entry point
│
├── assets/                  # Demo images used in README
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

# 🚀 Getting Started

## Prerequisites

- Python **3.10** or higher

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/shanzaashraf003/image-encryption-tool.git
cd image-encryption-tool
```

### 2. Install Dependencies

```bash
pip install customtkinter pillow
```

Or install using:

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python src/main.py
```

---

# 📖 How It Works

The encryption process follows three main steps:

## 1. Keystream Generation

The user-provided password is combined with an incremental counter and hashed repeatedly using **SHA-256** to generate a continuous stream of pseudo-random bytes.

This keystream is expanded until it matches the exact number of RGB bytes contained in the image.

---

## 2. Pixel Encryption

Each RGB channel of every pixel is encrypted independently using the XOR operation:

\[
Pixel_{encrypted}=Pixel_{original}\oplus KeyByte
\]

where:

- **Pixel_original** = Original pixel value
- **KeyByte** = Corresponding byte from the SHA-256 keystream
- **⊕** = Bitwise XOR operation

The output becomes visually indistinguishable from random noise while remaining a valid image file.

---

## 3. Decryption

XOR is a reversible operation.

Applying the **same password** generates the identical keystream, allowing the encrypted pixels to be restored perfectly:

\[
Pixel_{original}=Pixel_{encrypted}\oplus KeyByte
\]

Because:

\[
A\oplus B\oplus B=A
\]

No image quality is lost during this process.

---

# 📷 Workflow

1. Launch the application.
2. Browse and select an image.
3. Enter an encryption password.
4. Click **Encrypt**.
5. The encrypted image is saved automatically as a PNG file.
6. To restore the original image, select the encrypted image, enter the same password, and click **Decrypt**.

---

# 🔐 Security Notes

- Encryption strength depends on the secrecy of the user password.
- The application uses SHA-256-based keystream expansion to eliminate visible encryption patterns.
- Encrypted images should always be stored in **PNG format** to preserve every encrypted pixel value.
- Using an incorrect password will produce meaningless output rather than the original image.

---

# 📄 License

This project is distributed under the **MIT License**.

See the **LICENSE** file for additional details.

---

# 👩Author

**Shanza Ashraf**

Email: shanzaashraf003@gmail.com
GitHub: **https://github.com/shanzaashraf003**
linkedIn: **https://www.linkedin.com/in/shanzaashraf/**
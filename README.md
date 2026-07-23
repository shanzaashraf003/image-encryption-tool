# Image Encryption Tool 

A modern desktop application built with **Python**, **CustomTkinter**, and **Pillow** that provides secure, lossless image encryption and decryption using a SHA-256 derived XOR keystream.

---

## Features

* **Lossless XOR Encryption:** Encrypts raw RGB pixel data so the output remains a valid image file.
* **SHA-256 Keystream:** Uses pseudo-random key expansion so short passwords turn images into full static noise instead of basic color shifts.
* **Automatic Format Management:** Saves encrypted files as PNG to prevent lossy JPEG compression from corrupting pixel bit values.
* **Modern GUI:** Built with CustomTkinter featuring dark/light mode toggles, file previewing, progress tracking, and seamless workflow.
* **Smart File Tracking:** Automatically selects newly generated output files for instant decryption testing.

---

## 📁 Project Structure

```text
image-encryption-tool/
│
├── output/              # Directory where encrypted/decrypted images are saved
├── src/
│   ├── crypto.py        # XOR & SHA-256 keystream processing logic
│   ├── file_handler.py  # File validation & path generation
│   ├── gui.py           # CustomTkinter interface layout and events
│   └── main.py          # Application entry point
├── .gitignore           # Git ignore rules
├── LICENSE              # MIT License
├── README.md            # Project documentation
└── requirements.txt     # Dependency list
```

---

##  Getting Started

### Prerequisites

* Python 3.10 or higher

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/shanzaashraf003/image-encryption-tool.git](https://github.com/shanzaashraf003/image-encryption-tool.git)
   cd image-encryption-tool
   ```

2. **Install dependencies:**
   ```bash
   pip install customtkinter pillow
   ```

3. **Run the application:**
   ```bash
   python src/main.py
   ```

---

##  How It Works

1. **Keystream Generation:** The entered password is hashed alongside an incremental counter using SHA-256 to create a continuous stream of pseudo-random bytes matching the exact pixel count of the image.
2. **Pixel Transformation:** Each pixel channel $(R, G, B)$ is bitwise XOR'd with its corresponding keystream byte:
   $$\text{Pixel}_{\text{out}} = \text{Pixel}_{\text{in}} \oplus \text{KeyByte}$$
3. **Reversibility:** Applying the same operation again with the matching key perfectly restores the original pixel values.

---

##  License

Distributed under the MIT License. See `LICENSE` for more details.
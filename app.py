import streamlit as st
from PIL import Image, ImageGrab
import pytesseract
import cv2
import numpy as np
import requests
from io import BytesIO
import pyperclip 

# Inisisasi tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Judul
st.title("Scan Image")

# Pilih input: file upload atau URL
input_type = st.radio("Pilih sumber gambar:", ("Upload File", "Clipboard"))

image = None
if input_type == "Upload File":
    uploaded_file = st.file_uploader("Unggah gambar di sini", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
# Clipboard (hanya lokal)
elif input_type == "Clipboard":
    if st.button("Ambil Gambar dari Clipboard"):
        image = ImageGrab.grabclipboard()
        if image is None:
            st.warning("Clipboard tidak berisi gambar.")
            
# Jika ada gambar, lakukan OCR
if image is not None:
    st.image(image, caption="Gambar yang dipilih", use_container_width=True)

    # Konversi ke OpenCV
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Preprocessing otomatis
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Resize untuk meningkatkan akurasi OCR
    scale_percent = 150  # 150% ukuran asli
    width = int(gray.shape[1] * scale_percent / 100)
    height = int(gray.shape[0] * scale_percent / 100)
    gray = cv2.resize(gray, (width, height), interpolation=cv2.INTER_LINEAR)

    # Denoise & threshold
    gray = cv2.medianBlur(gray, 3)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # OCR
    text = pytesseract.image_to_string(thresh, lang="ind+eng")

    # Tampilkan hasil
    st.subheader("Hasil:")
    st.text_area("Teks yang terbaca:", text, height=200, key="ocr_text")

    # Tombol copy ke clipboard
    if st.button("📋 Salin ke Clipboard"):
        try:
            pyperclip.copy(text)
            st.success("Teks berhasil dicopy ke clipboard!")
        except Exception as e:
            st.error(f"Gagal copy ke clipboard: {e}")

else:
    st.info("Silakan unggah gambar atau masukkan URL terlebih dahulu.")
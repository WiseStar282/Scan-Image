import streamlit as st
from PIL import Image
import numpy as np
import easyocr
import pyperclip
import platform

# Judul
st.title("Scan Image (OCR Cepat)")

# Load EasyOCR sekali saja
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['id', 'en'], gpu=False)

reader = load_ocr()

# Pilih input: Upload atau Clipboard (Windows lokal)
input_type = st.radio("Pilih sumber gambar:", ("Upload File", "Clipboard"))

image = None

# Mengambil gambar dari upload atau clipboard
if input_type == "Upload File":
    uploaded_file = st.file_uploader("Unggah gambar di sini", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)

elif input_type == "Clipboard":
    if platform.system() != "Windows":
        st.warning("Clipboard hanya didukung di Windows. Silakan gunakan Upload File.")
    else:
        if st.button("Ambil gambar dari Clipboard"):
            from PIL import ImageGrab
            image = ImageGrab.grabclipboard()
            if image is None:
                st.warning("Clipboard tidak berisi gambar.")

# Jika ada gambar
if image is not None:
    st.image(image, caption="Gambar yang dipilih", use_container_width=True)

    # Resize gambar untuk OCR cepat
    max_side = 800
    width, height = image.size
    scale = min(max_side / width, max_side / height, 1)
    if scale < 1:
        new_size = (int(width * scale), int(height * scale))
        image = image.resize(new_size, Image.Resampling.LANCZOS)

    # Convert ke numpy array
    img_np = np.array(image)

    # OCR
    results = reader.readtext(img_np, detail=0)
    text = "\n".join(results)

    # Simpan hasil OCR di session_state
    st.session_state.ocr_text = text

    # Tampilkan hasil OCR
    st.subheader("Hasil OCR:")
    st.text_area("Teks yang terbaca:", text, height=200, key="ocr_text_display")

    # Tombol copy ke clipboard (lokal)
    if st.button("📋 Salin ke Clipboard"):
        try:
            pyperclip.copy(st.session_state.ocr_text)
            st.success("Teks berhasil dicopy ke clipboard!")
        except Exception as e:
            st.error(f"Gagal copy ke clipboard: {e}")

else:
    st.info("Silakan unggah gambar atau ambil dari clipboard terlebih dahulu.")

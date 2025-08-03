import streamlit as st
import pytesseract
import spacy
import cv2
import numpy as np
from PIL import Image
import os

# Load spaCy model with fallback download
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

st.set_page_config(page_title="Smart Redactor", layout="centered")
st.title("🛡️ Smart Redactor for Scanned Documents")
st.markdown("Upload a scanned image, and we’ll detect & redact personal information (names, dates, etc.)")

uploaded_file = st.file_uploader("📁 Upload Scanned Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(image)
    st.image(image, caption="📄 Original Image", use_column_width=True)

    # OCR: Extract text with positions
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    full_text = " ".join(data["text"])

    # NLP: Detect sensitive entities
    doc = nlp(full_text)
    sensitive_entities = [ent.text.strip() for ent in doc.ents if ent.label_ in ["PERSON", "GPE", "ORG", "DATE"]]
    st.markdown("### 🔍 Detected Sensitive Entities")
    st.write(sensitive_entities)

    # Redact image
    redacted_img = img_np.copy()
    for i, word in enumerate(data["text"]):
        if word.strip() in sensitive_entities:
            x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
            cv2.rectangle(redacted_img, (x, y), (x + w, y + h), (0, 0, 0), -1)

    st.image(redacted_img, caption="🕵️ Redacted Image", use_column_width=True)

    # Allow download
    result_image = Image.fromarray(redacted_img)
    st.download_button(
        label="📥 Download Redacted Image",
        data=result_image.tobytes(),
        file_name="redacted_output.png",
        mime="image/png"
    )

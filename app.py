import streamlit as st

st.set_page_config(page_title="Smart Redactor", layout="centered")

st.title("🛡️ Smart Redactor Demo")
st.write("Upload an image and see OCR + redaction (coming soon).")

uploaded_file = st.file_uploader("Upload a scanned image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    st.success("This is a placeholder — redaction logic will go here.")

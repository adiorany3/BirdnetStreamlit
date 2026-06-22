
import streamlit as st
import tempfile
import os

st.set_page_config(page_title="BirdNET Analyzer", layout="wide")

st.title("🐦 BirdNET Analyzer")

uploaded = st.file_uploader("Upload Audio", type=["wav","mp3","flac"])

if uploaded:
    st.audio(uploaded)

    if st.button("Analisis"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(uploaded.read())
            audio_path = tmp.name

        try:
            st.info("Pastikan package birdnet dan model sudah tersedia.")

            try:
                from birdnet.models import ModelV2M4

                model = ModelV2M4()
                results = model.predict(audio_path)

                st.success("Analisis selesai")
                st.write(results)

            except Exception as e:
                st.error(f"BirdNET belum terkonfigurasi penuh: {e}")

        finally:
            if os.path.exists(audio_path):
                os.remove(audio_path)

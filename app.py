import streamlit as st

st.set_page_config(page_title="BirdNET Analyzer", layout="wide")

st.title("🐦 BirdNET Bird Sound Analyzer")
st.write("Cloud-ready template untuk Streamlit Community Cloud")

audio = st.file_uploader("Upload Audio", type=["wav","mp3","flac"])

if audio:
    st.audio(audio)

    if st.button("Analisis"):
        st.info("Hubungkan ke BirdNET Analyzer pada tahap berikutnya.")
        st.success("Template berhasil berjalan.")

import streamlit as st
import pandas as pd
import tempfile
import os

from birdnetlib import Recording
from birdnetlib.analyzer import Analyzer

st.set_page_config(
    page_title="BirdNET Analyzer",
    page_icon="🐦",
    layout="wide"
)

st.title("🐦 BirdNET Bird Sound Analyzer")

st.markdown(
    """
    Upload file audio burung dan sistem akan mencoba
    mengidentifikasi spesies menggunakan BirdNET.
    """
)

uploaded_file = st.file_uploader(
    "Upload Audio",
    type=["wav", "mp3", "flac", "ogg"]
)

if uploaded_file:

    st.audio(uploaded_file)

    if st.button("Analisis Burung"):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        ) as tmp:

            tmp.write(uploaded_file.read())
            audio_path = tmp.name

        try:

            with st.spinner(
                "Menganalisis suara burung..."
            ):

                analyzer = Analyzer()

                recording = Recording(
                    analyzer,
                    audio_path,
                    min_conf=0.25
                )

                recording.analyze()

                detections = recording.detections

            if len(detections) == 0:

                st.warning(
                    "Tidak ditemukan spesies burung."
                )

            else:

                df = pd.DataFrame(detections)

                st.success(
                    f"{len(df)} deteksi ditemukan"
                )

                st.dataframe(
                    df,
                    use_container_width=True
                )

                st.subheader("Top Hasil")

                if "confidence" in df.columns:

                    st.bar_chart(
                        df.set_index(
                            df.columns[0]
                        )["confidence"]
                    )

                csv = df.to_csv(
                    index=False
                ).encode("utf-8")

                st.download_button(
                    "Download CSV",
                    csv,
                    file_name="birdnet_results.csv",
                    mime="text/csv"
                )

        except Exception as e:

            st.error(
                f"Terjadi kesalahan: {e}"
            )

        finally:

            if os.path.exists(audio_path):
                os.remove(audio_path)

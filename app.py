import streamlit as st
import pandas as pd
import tempfile
import os

from birdnetlib import Recording
from birdnetlib.analyzer import Analyzer

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="BirdNET Analyzer",
    page_icon="🐦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# HIDE STREAMLIT ELEMENTS
# ==========================================

st.markdown("""
<style>

/* Hide Streamlit menu */
#MainMenu {
    visibility: hidden;
}

/* Hide default footer */
footer {
    visibility: hidden;
}

/* Hide header */
header {
    visibility: hidden;
}

/* Hide toolbar */
[data-testid="stToolbar"] {
    display: none;
}

/* Hide decoration */
[data-testid="stDecoration"] {
    display: none;
}

/* Hide status widget */
[data-testid="stStatusWidget"] {
    display: none;
}

/* Reduce top spacing */
.block-container {
    padding-top: 1rem;
    padding-bottom: 4rem;
}

/* Custom footer */
.custom-footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    text-align: center;
    padding: 10px;
    background-color: white;
    border-top: 1px solid #e5e5e5;
    font-size: 13px;
    z-index: 9999;
}

</style>

<div class="custom-footer">
    © 2026 BirdNET Analyzer | Developed by Galuh Adi Insani
</div>
""", unsafe_allow_html=True)

# ==========================================
# TITLE
# ==========================================

st.title("🐦 BirdNET Bird Sound Analyzer")

st.markdown("""
Upload file audio burung dan sistem akan mencoba
mengidentifikasi spesies menggunakan BirdNET AI.
""")

# ==========================================
# FILE UPLOAD
# ==========================================

uploaded_file = st.file_uploader(
    "Upload Audio",
    type=["wav", "mp3", "flac", "ogg"]
)

# ==========================================
# PROCESS
# ==========================================

if uploaded_file:

    st.audio(uploaded_file)

    if st.button("🔍 Analisis Burung"):

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

            # ==================================
            # RESULT
            # ==================================

            if len(detections) == 0:

                st.warning(
                    "Tidak ada spesies burung yang terdeteksi."
                )

            else:

                df = pd.DataFrame(detections)

                st.success(
                    f"{len(df)} deteksi ditemukan"
                )

                st.subheader("📋 Hasil Deteksi")

                st.dataframe(
                    df,
                    use_container_width=True
                )

                # Confidence chart

                if "confidence" in df.columns:

                    st.subheader("📈 Confidence")

                    chart_df = df.copy()

                    species_col = df.columns[0]

                    st.bar_chart(
                        chart_df.set_index(
                            species_col
                        )["confidence"]
                    )

                # CSV download

                csv = df.to_csv(
                    index=False
                ).encode("utf-8")

                st.download_button(
                    label="⬇ Download CSV",
                    data=csv,
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

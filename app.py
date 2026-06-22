import streamlit as st
import pandas as pd
import tempfile
import os
from datetime import datetime

from birdnetlib import Recording
from birdnetlib.analyzer import Analyzer

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="BirdNET Analyzer",
    page_icon="🐦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================================================
# CUSTOM CSS
# ==================================================

year = datetime.now().year

st.markdown(
    f"""
    <style>

    #MainMenu {{
        visibility: hidden;
    }}

    footer {{
        visibility: hidden;
    }}

    header {{
        visibility: hidden;
    }}

    [data-testid="stToolbar"] {{
        display: none;
    }}

    [data-testid="stDecoration"] {{
        display: none;
    }}

    [data-testid="stStatusWidget"] {{
        display: none;
    }}

    .block-container {{
        padding-top: 1rem;
        padding-bottom: 5rem;
    }}

    .custom-footer {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        text-align: center;
        padding: 10px;
        background: white;
        border-top: 1px solid #ddd;
        font-size: 13px;
        z-index: 9999;
    }}

st.divider()

col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.markdown(
        f"""
        <div style='text-align:center'>
        <b>BirdNET Analyzer</b><br>
        © {year} Developed by Adi Orany
        </div>
        """,
        unsafe_allow_html=True
    )
)

# ==================================================
# TITLE
# ==================================================

st.title("🐦 BirdNET Bird Sound Analyzer")

st.markdown(
    """
    Upload file audio burung dan sistem akan mencoba
    mengidentifikasi spesies menggunakan BirdNET AI.
    """
)

# ==================================================
# UPLOAD
# ==================================================

uploaded_file = st.file_uploader(
    "Upload Audio",
    type=["wav", "mp3", "flac", "ogg"]
)

# ==================================================
# ANALYSIS
# ==================================================

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

            # ======================================
            # RESULT
            # ======================================

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

                # ==================================
                # CHART
                # ==================================

                if "confidence" in df.columns:

                    st.subheader("📈 Confidence")

                    if "common_name" in df.columns:

                        chart_df = df[
                            ["common_name", "confidence"]
                        ]

                        st.bar_chart(
                            chart_df.set_index(
                                "common_name"
                            )
                        )

                    elif "scientific_name" in df.columns:

                        chart_df = df[
                            ["scientific_name", "confidence"]
                        ]

                        st.bar_chart(
                            chart_df.set_index(
                                "scientific_name"
                            )
                        )

                # ==================================
                # DOWNLOAD CSV
                # ==================================

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

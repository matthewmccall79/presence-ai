import streamlit as st
import soundfile as sf
import pandas as pd
emotion_descriptions = {
    "Excited": "This recording shows a high-energy pattern that may suggest playfulness, anticipation, or stimulation.",
    "Alert": "This recording shows a sharper attention-based pattern that may suggest curiosity, awareness, or reaction to something nearby.",
    "Anxious": "This recording shows a more tense or unstable pattern that may suggest stress, uncertainty, or discomfort."
}
from analyzer import analyze_audio
from limiter import check_limit
from history import init_db, save_analysis, get_history, clear_history
st.set_page_config(page_title="Presence AI", layout="centered")
st.markdown("""
<style>
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }

    .stDownloadButton > button {
        border-radius: 10px;
        font-weight: 600;
    }

    .stAlert {
        border-radius: 12px;
    }

    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: bold;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)
init_db()
st.title("Presence AI")
st.caption("AI-driven emotion interpretation for pets")
st.info("Experimental AI tool for entertainment and behavioral insight only. Not a veterinary diagnosis")
st.subheader("Record Pet Audio")
if "recording_key" not in st.session_state:
    st.session_state.recording_key = 0
recorded_audio = st.audio_input(
    "Record your pet's sound",
    key=f"audio_recorder_{st.session_state.recording_key}"
)
if recorded_audio is not None:
    st.audio(recorded_audio, format="audio/wav")
    with st.spinner("Analyzing pet emotion..."):
        result = analyze_audio(recorded_audio)
    save_analysis("Recorded Audio", result)
    recorded_audio.seek(0)
    audio_data, sample_rate = sf.read(recorded_audio)

    if len(audio_data.shape) > 1:
        audio_data = audio_data.mean(axis=1)

    plot_step = max(1, len(audio_data) // 2000)
    plot_data = audio_data[::plot_step]

    waveform_df = pd.DataFrame({
        "sample": range(len(plot_data)),
        "amplitude": plot_data
    })

    st.subheader("Waveform Preview")
    st.line_chart(waveform_df.set_index("sample"))

    top_emotion = result["top_emotion"]
    confidence = result["probabilities"][top_emotion]

    st.subheader("Recorded Audio Result")
    st.success(top_emotion)
    st.metric("Confidence", f"{confidence:.2f}%")
    st.subheader("What This May Mean")
    st.write(emotion_descriptions.get(top_emotion, "No description available for this result."))
    if st.button("Reset Recording"):
        st.session_state.recording_key += 1
        st.rerun()
    st.subheader("Emotion Probabilities")
    for emotion, value in result["probabilities"].items():
        st.progress(value / 100)
        st.write(f"{emotion}: {value}%")

    st.subheader("Extracted Features")
    st.write(f"Duration: {result['features']['duration']:.2f} seconds")
    st.write(f"RMS: {result['features']['rms']:.4f}")
    st.write(f"Zero Crossing Rate: {result['features']['zcr']:.4f}")
    st.write(f"Spectral Centroid: {result['features']['spectral_centroid']:.4f}")
    st.write(f"Energy Variance: {result['features']['energy_variance']:.4f}")

uploaded_file = st.file_uploader("Upload your pet's sound", type=["wav", "flac"])

if uploaded_file:
    if not check_limit():
        st.error("Daily free limit reached. Upgrade for unlimited analyses.")
        st.stop()

    result = analyze_audio(uploaded_file)
    save_analysis(uploaded_file.name, result)
    top_emotion = result["top_emotion"]
    confidence = result["probabilities"][top_emotion]
    uploaded_file.seek(0)
    audio_data, sample_rate = sf.read(uploaded_file)

    if len(audio_data.shape) > 1:
        audio_data = audio_data.mean(axis=1)

    plot_step = max(1, len(audio_data) // 2000)
    plot_data = audio_data[::plot_step]

    st.subheader("Waveform Preview")
    st.write(f"Showing {len(plot_data)} downsample points from {len(audio_data)} total samples.")

    st.subheader("Emotion Probabilities")

    for emotion, value in result["probabilities"].items():
        st.progress(value / 100)
        st.write(f"{emotion}: {value}%")

    st.subheader("Primary Emotion")
    st.success(top_emotion)
    st.metric("Confidence", f"{confidence:.2f}%")
    st.subheader("What This May Mean")
    st.write(emotion_descriptions.get(top_emotion, "No description available for this result."))
    st.subheader("Extracted Features")
    st.write(f"Duration: {result['features']['duration']:.2f} seconds")
    st.write(f"RMS: {result['features']['rms']:.4f}")
    st.write(f"Zero Crossing Rate: {result['features']['zcr']:.4f}")
    st.write(f"Spectral Centroid: {result['features']['spectral_centroid']:.4f}")
    st.write(f"Energy Variance: {result['features']['energy_variance']:.4f}")

st.subheader("Analysis History")
if st.button("Clear History"):
    clear_history()
    st.rerun()

history_rows = get_history()

if history_rows:
    history_df = pd.DataFrame(
        history_rows,
        columns=["Date/Time", "File", "Emotion"]
    )

    csv = history_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download History as CSV",
        data=csv,
        file_name="presence_ai_history.csv",
        mime="text/csv",
    )
    st.dataframe(history_df, use_container_width=True)

    st.subheader("Emotion Trend")

    emotion_counts = history_df["Emotion"].value_counts()

    st.bar_chart(emotion_counts)

else:
    st.write("No analysis history yet.")


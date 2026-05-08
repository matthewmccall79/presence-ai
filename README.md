# Presence AI

AI-generated pet audio emotion analyzer built with Streamlit.

## Live Demo

[Launch Presence AI]{https://presence-ai.streamlit.app/)

## Features

- Record pet audio directly in browser
- Upload WAV and FLAC audio files
- AI-based emotion classification
- Emotion confidence scoring
- Audio waveform visualization
- Emotion probability breakdown
- Extracted audio feature analysis
- Analysis history tracking
- CSV export support
- Emotion trend visualization

## Supported Emotions

- Excited
- Alert
- Anxious
- Calm

## Tech Stack

- Python
- Streamlit
- Pandas
- SoundFile
- SQLite

## How It Works

Presence AI analyzes uploaded or recorded pet audio and extracts several audio features including:

- RMS Energy
- Zero Crossing Rate
- Spectral Centroid
- Energy Variance
- Duration

These features are processed through a lightweight emotion engine that estimates likely emotional states from pet vocalizations.

## Installation

Clone the repository:

```bash
git clone https://github.com/matthewmccall79/presence-ai.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## Disclaimer

This application is for entertainment and behavioral insight purposes only and is not intended for veterinary diagnosis.

## Future Improvements

- Machine learning model integration
- Breed-specific analysis
- Bark classification
- Real-time microphone streaming
- Mobile optimization
- Cloud deployment
- User authentication

## Author

Matthew McCall

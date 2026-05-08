import numpy as np
import soundfile as sf

def extract_features(file):
    y, sr = sf.read(file)

    if len(y.shape) > 1:
        y = np.mean(y, axis=1)

    duration = len(y) / sr

    rms = np.sqrt(np.mean(y**2))
    zcr = np.mean(np.abs(np.diff(np.sign(y))))
    spectral_centroid = np.mean(np.abs(np.fft.rfft(y)))
    energy_variance = np.var(y)

    return {
        "duration": duration,
        "rms": rms,
        "zcr": zcr,
        "spectral_centroid": spectral_centroid,
        "energy_variance": energy_variance,
    }
def score_emotions(features):
    score_excited = features["rms"] * 2 + features["zcr"] * 3
    score_alert = features["spectral_centroid"] * 0.00001
    score_anxious = features["energy_variance"] * 5

    total = score_excited + score_alert + score_anxious + 1e-6

    return {
        "Excited": round((score_excited / total) * 100, 2),
        "Alert": round((score_alert / total) * 100, 2),
        "Anxious": round((score_anxious / total) * 100, 2),
    }

def analyze_audio(file):
    features = extract_features(file)
    probabilities = score_emotions(features)

    top_emotion = max(probabilities, key=probabilities.get)

    return {
        "top_emotion": top_emotion,
        "probabilities": probabilities,
        "features": features
    }

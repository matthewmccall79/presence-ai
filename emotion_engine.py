def score_emotion(duration, intensity, burst):
    scores = {
        "Alert / Protective": 0,
        "Playful / Excited": 0,
        "Anxious / Distressed": 0,
        "Lonely / Seeking Attention": 0
    }

    if intensity > 0.7 and bursts >= 5:
        scores["Alert / Protective"] += 2

    if duration < 3 and bursts >= 3:
        scores["Playful / Excited"] += 2

    if duration > 8 and burst >= 3:
        scores["Anxious / Distressed"] += 2

    return max(scores, key=scores.get)
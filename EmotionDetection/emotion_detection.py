"""Detect emotions in text with the Watson NLP EmotionPredict service."""
import json
import requests


def emotion_detector(text_to_analyze):
    """Return emotion scores and the dominant emotion for the given text.

    The Watson NLP endpoint is called with the supplied statement. A blank or
    rejected statement (HTTP 400) returns every score and the dominant emotion
    as None.

    Args:
        text_to_analyze: Statement submitted for emotion detection.

    Returns:
        Dictionary with anger, disgust, fear, joy, sadness, and dominant_emotion.
    """
    url = (
        "https://sn-watson-emotion.labs.skills.network/v1/"
        "watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj = {"raw_document": {"text": text_to_analyze}}
    response = requests.post(url, json=myobj, headers=header, timeout=10)

    if response.status_code == 400:
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }

    formatted_response = json.loads(response.text)
    emotions = formatted_response["emotionPredictions"][0]["emotion"]
    anger_score = emotions["anger"]
    disgust_score = emotions["disgust"]
    fear_score = emotions["fear"]
    joy_score = emotions["joy"]
    sadness_score = emotions["sadness"]
    emotion_scores = {
        "anger": anger_score,
        "disgust": disgust_score,
        "fear": fear_score,
        "joy": joy_score,
        "sadness": sadness_score,
    }
    emotion_scores["dominant_emotion"] = max(emotion_scores, key=emotion_scores.get)
    return emotion_scores

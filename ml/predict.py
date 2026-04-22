import os
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model")

# load model
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

model.eval()

def convert_to_phq_score(p_negative, p_neutral, p_positive):
    score = (p_negative * 1.0) + (p_neutral * 0.4)

    if score < 0.3:
        return 0
    elif score < 0.7:
        return 1
    elif score < 1.1:
        return 2
    else:
        return 3

def classify_phq(total_score):
    if total_score <= 4:
        return "Minimal"
    elif total_score <= 9:
        return "Mild"
    elif total_score <= 14:
        return "Moderate"
    elif total_score <= 19:
        return "Moderately Severe"
    else:
        return "Severe"


def predict_text(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)[0]

    p_negative = probs[0].item()
    p_neutral = probs[1].item()
    p_positive = probs[2].item()

    phq_score = convert_to_phq_score(p_negative, p_neutral, p_positive)

    return {
        "probabilities": {
            "negative": p_negative,
            "neutral": p_neutral,
            "positive": p_positive
        },
        "phq_score": phq_score
    }

def predict_multiple(text_list):
    text_list = [t for t in text_list if t.strip() != ""]

    if not text_list:
        return {"error": "No valid input"}

    total_score = 0
    details = []

    for text in text_list:
        result = predict_text(text)
        total_score += result["phq_score"]
        details.append(result)

    avg_score = total_score / len(text_list)
    category = classify_phq(total_score)

    return {
        "total_score": total_score,
        "average_score": avg_score,
        "category": category,
        "interpretation": interpretation(category),
        "details": details
    }

def interpretation(category):
    mapping = {
        "Minimal": "Kondisi mental dalam batas normal.",
        "Mild": "Terdapat gejala ringan, disarankan menjaga pola hidup sehat.",
        "Moderate": "Perlu perhatian lebih terhadap kesehatan mental.",
        "Moderately Severe": "Disarankan konsultasi dengan profesional.",
        "Severe": "Segera cari bantuan profesional."
    }
    return mapping.get(category, "")
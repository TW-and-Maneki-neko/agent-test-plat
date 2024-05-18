import json
import os
import requests
from config import NLU_API_URL

def load_test_cases(agent_dir):
    test_cases = []
    for file_name in os.listdir(agent_dir):
        if file_name.endswith(".json"):
            file_path = os.path.join(agent_dir, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                test_cases.extend(json.load(file))
    return test_cases

def save_test_cases(file_path, test_cases):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(test_cases, file, ensure_ascii=False, indent=4)

def test_nlu(test_cases):
    results = []
    for case in test_cases:
        response = requests.post(NLU_API_URL, json={"input_text": case["input"]})
        response_data = response.json()
        intent_correct = response_data["intent_label"] == case["expected_intent"]
        slots_correct = response_data["slot_labels"] == case["expected_slots"]
        results.append({
            "input": case["input"],
            "expected_intent": case["expected_intent"],
            "actual_intent": response_data["intent_label"],
            "expected_slots": case["expected_slots"],
            "actual_slots": response_data["slot_labels"],
            "confidence": response_data["intent_confidence"],
            "intent_correct": intent_correct,
            "slots_correct": slots_correct
        })
    return results

def highlight_text(text, color):
    return f'<span style="color:{color}">{text}</span>'

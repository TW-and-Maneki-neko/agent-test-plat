import json
import os
import requests
from config import NLU_API_URL

def load_test_cases(agent_dir, domain):
    test_cases = []
    test_cases_dir = os.path.join(agent_dir, "auto_test")
    test_cases_file = os.path.join(test_cases_dir, f"{domain}.json")
    if not os.path.exists(test_cases_dir):
        os.makedirs(test_cases_dir)
        return []
    
    if not os.path.exists(test_cases_file):
        return []
    
    with open(test_cases_file, "r", encoding="utf-8") as file:
        test_cases.extend(json.load(file))
    return test_cases

def save_test_cases(file_path, test_cases):
    if not test_cases:  # 检查是否为空
        return
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

def highlight_slot(text, slot_name, slot_value, color):
    return f'<span style="color:{color};font-size:0.9em;position:relative;display:inline-block">{slot_value}<span style="font-size:0.7em;color:gray;position:absolute;left:0;bottom:-1em">{slot_name}</span></span>'
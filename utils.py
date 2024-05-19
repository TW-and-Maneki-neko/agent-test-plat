from collections import defaultdict
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


def calculate_metrics(nlu_results):
    # 用于统计各个意图的准确率和召回率
    intent_tp = defaultdict(int)
    intent_fp = defaultdict(int)
    intent_fn = defaultdict(int)

    # 用于统计各个意图中槽位的准确率和召回率
    slot_tp = defaultdict(lambda: defaultdict(int))
    slot_fp = defaultdict(lambda: defaultdict(int))
    slot_fn = defaultdict(lambda: defaultdict(int))

    for result in nlu_results:
        expected_intent = result["expected_intent"]
        actual_intent = result["actual_intent"]
        expected_slots = result["expected_slots"]
        actual_slots = result["actual_slots"]

        # 统计意图的准确率和召回率
        if expected_intent == actual_intent:
            intent_tp[expected_intent] += 1
        else:
            intent_fp[actual_intent] += 1
            intent_fn[expected_intent] += 1

        # 统计槽位的准确率和召回率
        for slot_name, slot_details in expected_slots.items():
            expected_slot_value = slot_details["value"]
            if slot_name in actual_slots:
                actual_slot_value = actual_slots[slot_name]["value"]
                if expected_slot_value == actual_slot_value:
                    slot_tp[expected_intent][slot_name] += 1
                else:
                    slot_fp[expected_intent][slot_name] += 1
                    slot_fn[expected_intent][slot_name] += 1
            else:
                slot_fn[expected_intent][slot_name] += 1

    stats = {
        'intent_tp': intent_tp,
        'intent_fp': intent_fp,
        'intent_fn': intent_fn,
        'slot_tp': slot_tp,
        'slot_fp': slot_fp,
        'slot_fn': slot_fn
    }

    return stats
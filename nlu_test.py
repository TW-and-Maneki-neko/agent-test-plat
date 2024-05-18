import streamlit as st
import json
import requests
import os
from config import TEST_CASE_DIR, NLU_API_URL

NLU_TEST_CASES_FILE = os.path.join(TEST_CASE_DIR, "nlu")

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

def nlu_test_page():
    st.header("NLU测试")
    st.write("添加并运行针对NLU的测试用例。")

    nlu_test_cases = load_test_cases(NLU_TEST_CASES_FILE)

    st.write("现有测试用例：")
    if nlu_test_cases:
        case_columns = st.columns(len(nlu_test_cases[0]))
        headers = list(nlu_test_cases[0].keys())
        for col, header in zip(case_columns, headers):
            col.write(header)

        for case in nlu_test_cases:
            row_cols = st.columns(len(case))
            for col, value in zip(row_cols, case.values()):
                col.write(str(value))
    else:
        st.write("暂无测试用例")

    new_nlu_case_input = st.text_input("输入NLU测试用例")
    new_nlu_case_expected_intent = st.text_input("期望意图")
    new_nlu_case_expected_slots = st.text_input("期望槽位 (JSON格式)")

    if st.button("添加NLU测试用例"):
        try:
            expected_slots = json.loads(new_nlu_case_expected_slots)
            new_nlu_case = {
                "input": new_nlu_case_input,
                "expected_intent": new_nlu_case_expected_intent,
                "expected_slots": expected_slots
            }
            nlu_test_cases.append(new_nlu_case)
            save_test_cases(NLU_TEST_CASES_FILE, nlu_test_cases)
            st.success("NLU测试用例已添加并保存。")
        except json.JSONDecodeError:
            st.error("期望槽位格式错误，请输入有效的JSON格式。")

    if st.button("运行NLU测试"):
        nlu_results = test_nlu(nlu_test_cases)
        st.write("测试结果：")
        for result in nlu_results:
            st.write(f"输入: {result['input']}")
            st.write(f"期望意图: {result['expected_intent']}, 实际意图: {result['actual_intent']}, {'正确' if result['intent_correct'] else '错误'}")
            st.write(f"期望槽位: {result['expected_slots']}, 实际槽位: {result['actual_slots']}, {'正确' if result['slots_correct'] else '错误'}")
            st.write(f"置信度: {result['confidence']}")
            st.markdown("---")
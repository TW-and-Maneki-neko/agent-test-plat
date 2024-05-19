import streamlit as st
import json
import requests
import os
from config import AGENT_PROJECT_DIR, AGENT_API_URL

E2E_TEST_CASES_FILE = os.path.join(AGENT_PROJECT_DIR, "e2e_test_cases.json")


def load_test_cases(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def save_test_cases(file_path, test_cases):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(test_cases, file, ensure_ascii=False, indent=4)

def test_agent_response(test_cases):
    results = []
    for case in test_cases:
        response = requests.post(AGENT_API_URL, json={"input": case["input"]})
        response_data = response.json()
        is_correct = response_data["reply"] == case["expected"]
        results.append({"input": case["input"], "expected": case["expected"], "actual": response_data["reply"], "correct": is_correct})
    return results

def e2e_test_page():
    st.header("E2E测试")
    st.write("添加并运行针对Agent回复的测试用例。")
    
    e2e_test_cases = load_test_cases(E2E_TEST_CASES_FILE)
    
    st.write("现有测试用例：")
    st.json(e2e_test_cases)
    
    new_case_input = st.text_input("输入测试用例")
    new_case_expected = st.text_input("期望回复")
    
    if st.button("添加测试用例"):
        new_case = {"input": new_case_input, "expected": new_case_expected}
        e2e_test_cases.append(new_case)
        save_test_cases(E2E_TEST_CASES_FILE, e2e_test_cases)
        st.success("测试用例已添加并保存。")
    
    if st.button("运行E2E测试"):
        e2e_results = test_agent_response(e2e_test_cases)
        st.write("测试结果：")
        st.json(e2e_results)

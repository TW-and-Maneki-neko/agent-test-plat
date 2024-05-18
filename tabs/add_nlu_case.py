import streamlit as st
import json
from config import NLU_TEST_CASES_FILE
from utils import load_test_cases, save_test_cases

def add_nlu_case_tab():
    st.header("添加测试用例")
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
            nlu_test_cases = load_test_cases(NLU_TEST_CASES_FILE)
            nlu_test_cases.append(new_nlu_case)
            save_test_cases(NLU_TEST_CASES_FILE, nlu_test_cases)
            st.success("NLU测试用例已添加并保存。")
        except json.JSONDecodeError:
            st.error("期望槽位格式错误，请输入有效的JSON格式。")

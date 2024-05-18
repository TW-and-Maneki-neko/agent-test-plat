import streamlit as st
from config import NLU_TEST_CASES_FILE
from utils import load_test_cases, highlight_text, test_nlu

def nlu_test_cases_tab():
    st.header("现有测试用例")
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

    if st.button("运行NLU测试"):
        nlu_results = test_nlu(nlu_test_cases)
        st.write("测试结果：")
        for result in nlu_results:
            input_text = result["input"]
            expected_intent = result["expected_intent"]
            actual_intent = result["actual_intent"]
            expected_slots = result["expected_slots"]
            actual_slots = result["actual_slots"]
            confidence = result["confidence"]

            intent_color = "green" if expected_intent == actual_intent else "red"
            confidence_color = "green" if confidence >= 0.7 else "yellow" if confidence >= 0.5 else "red"

            st.write(f"输入: {input_text}")
            st.markdown(f"{highlight_text(actual_intent, intent_color)}", unsafe_allow_html=True)

            # 在输入文本中高亮显示实体
            highlighted_input = input_text
            for slot_name, slot_details in actual_slots.items():
                slot_value = slot_details["value"]
                highlighted_input = highlighted_input.replace(slot_value, highlight_text(slot_value, confidence_color))
            st.markdown(f"{highlighted_input}", unsafe_allow_html=True)

            st.markdown("---")
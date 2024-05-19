import streamlit as st
from collections import defaultdict

from config import NLU_TEST_CASES_FILE
from utils import load_test_cases, highlight_slot, test_nlu

def nlu_test_cases_tab():
    st.header("运行 NLU 测试")

    nlu_test_cases = load_test_cases(NLU_TEST_CASES_FILE)

    # 统计各个意图的测试用例数量
    intent_counts = {}
    for case in nlu_test_cases:
        intent = case["expected_intent"]
        intent_counts[intent] = intent_counts.get(intent, 0) + 1

    st.write("测试用例意图统计：")
    for intent, count in intent_counts.items():
        percentage = (count / len(nlu_test_cases)) * 100
        st.write(f"- {intent}: {count} 个用例 ({percentage:.2f}%)")
    
    st.markdown("---")

    if st.button("运行NLU测试"):
        nlu_results = test_nlu(nlu_test_cases)
        st.write("测试结果：")

        # 创建表格
        result_table = "<table>"
        result_table += "<tr><th>输入</th><th>实际意图</th><th>实际槽位</th><th>置信度</th></tr>"

        # 用于统计各个意图的准确率和召回率
        intent_tp = defaultdict(int)
        intent_fp = defaultdict(int)
        intent_fn = defaultdict(int)

        # 用于统计各个意图中槽位的准确率和召回率
        slot_tp = defaultdict(lambda: defaultdict(int))
        slot_fp = defaultdict(lambda: defaultdict(int))
        slot_fn = defaultdict(lambda: defaultdict(int))

        for result in nlu_results:
            input_text = result["input"]
            expected_intent = result["expected_intent"]
            actual_intent = result["actual_intent"]
            expected_slots = result["expected_slots"]
            actual_slots = result["actual_slots"]
            confidence = result["confidence"]

            intent_color = "green" if expected_intent == actual_intent else "red"
            confidence_color = "green" if confidence >= 0.7 else "yellow" if confidence >= 0.5 else "red"

            # 在输入文本中高亮显示实体
            highlighted_input = input_text
            for slot_name, slot_details in actual_slots.items():
                slot_value = slot_details["value"]
                highlighted_input = highlighted_input.replace(slot_value, highlight_slot(input_text, slot_name, slot_value, confidence_color))

            result_table += f"<tr><td>{input_text}</td><td style='color:{intent_color}'>{actual_intent}</td><td>{highlighted_input}</td><td style='color:{confidence_color}'>{confidence}</td></tr>"

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

        result_table += "</table>"
        st.markdown(result_table, unsafe_allow_html=True)

        st.markdown("---")

        # 计算并显示各个意图的准确率和召回率
        st.write("各个意图的准确率和召回率：")
        for intent, count in intent_counts.items():
            tp = intent_tp[intent]
            fp = intent_fp[intent]
            fn = intent_fn[intent]
            precision = tp / (tp + fp) if tp + fp > 0 else 0
            recall = tp / (tp + fn) if tp + fn > 0 else 0
            st.write(f"- {intent}: 准确率={precision:.2f}, 召回率={recall:.2f}")

        # 计算并显示各个意图中槽位的准确率和召回率
        st.write("各个意图中槽位的准确率和召回率：")
        for intent in intent_counts:
            st.write(f"- {intent}:")
            for slot in set(slot_tp[intent].keys()) | set(slot_fp[intent].keys()) | set(slot_fn[intent].keys()):
                tp = slot_tp[intent][slot]
                fp = slot_fp[intent][slot]
                fn = slot_fn[intent][slot]
                precision = tp / (tp + fp) if tp + fp > 0 else 0
                recall = tp / (tp + fn) if tp + fn > 0 else 0
                st.write(f"  - {slot}: 准确率={precision:.2f}, 召回率={recall:.2f}")
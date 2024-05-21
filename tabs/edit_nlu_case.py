import os
import streamlit as st
import pandas as pd
from config import AGENT_PROJECT_DIR
from utils import load_test_cases, save_test_cases

def process_row(row):
    # 合并列为 JSON 字符串
    slots = {}
    
    for col, value in row.items():
        if '.' in col:
            slot, sub_key = col.split('.', 1)
            # if value is not nan
            if pd.notna(value):
                if slot not in slots:
                    slots[slot] = {}
                slots[slot][sub_key] = value
        else:
            if col not in ['input', 'expected_intent'] and pd.notna(value):
                slots[col] = {"value": value}
    return slots

def edit_nlu_case_tab():
    st.header("NLU 测试用例")

    # 加载现有测试用例
    nlu_test_cases = load_test_cases(AGENT_PROJECT_DIR, 'nlu')
    test_cases_dir = os.path.join(AGENT_PROJECT_DIR, "auto_test")
    test_cases_file = os.path.join(test_cases_dir, f"nlu.json")

    # 将测试用例转换为 DataFrame
    df = pd.DataFrame(nlu_test_cases)

    # 展开 expected_slots 列
    df = df.join(pd.json_normalize(df['expected_slots']))
    df = df.drop('expected_slots', axis=1)

    # 显示测试用例
    edited_df = st.data_editor(df, num_rows="dynamic")

    # 保存编辑
    if st.button("保存修改"):
        try:
            edited_df['expected_slots'] = edited_df.apply(lambda row: process_row(row.drop(['input', 'expected_intent'])), axis=1)
            edited_test_cases = edited_df[['input', 'expected_intent', 'expected_slots']].to_dict("records")
            save_test_cases(test_cases_file, edited_test_cases)
            st.success("测试用例已保存。")
        except Exception as e:
            st.error(f"保存失败: {e}")
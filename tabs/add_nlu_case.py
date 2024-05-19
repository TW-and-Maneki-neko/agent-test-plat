import streamlit as st
import pandas as pd
from config import AGENT_PROJECT_DIR
from utils import load_test_cases, save_test_cases

def add_nlu_case_tab():
    st.header("NLU 测试用例")

    # 加载现有测试用例
    nlu_test_cases = load_test_cases(AGENT_PROJECT_DIR, 'nlu')

    # 将测试用例转换为 DataFrame
    df = pd.DataFrame(nlu_test_cases)

    # 显示测试用例
    edited_df = st.data_editor(df, num_rows="dynamic")

    # 保存编辑
    if st.button("保存修改"):
        try:
            edited_test_cases = edited_df.to_dict("records")
            save_test_cases(AGENT_PROJECT_DIR, 'nlu', edited_test_cases)
            st.success("测试用例已保存。")
        except Exception as e:
            st.error(f"保存失败: {e}")
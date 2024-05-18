import streamlit as st
import requests

from config import AGENT_API_URL

def agent_interaction_page():
    st.header("与Agent对话")
    st.write("直接与Agent进行对话，并生成测试用例。")
    user_input = st.text_input("输入")
    if st.button("发送"):
        response = requests.post(AGENT_API_URL, json={"input": user_input})
        response_data = response.json()
        st.write("Agent回复：")
        st.write(response_data["reply"])
        if st.button("生成测试用例"):
            generated_case = {"input": user_input, "expected": response_data["reply"]}
            st.write("生成的测试用例：")
            st.json(generated_case)

import streamlit as st
import requests
import uuid
import json
import os
from config import AGENT_API_URL, AGENT_PROJECT_DIR

# 定义一个函数来调用Agent接口
def call_agent(session_id, user_input):
    payload = {
        "session_id": session_id,
        "user_input": user_input
    }
    response = requests.post(AGENT_API_URL, json=payload)
    return response.json()

# 初始化会话记录文件路径
test_cases_dir = os.path.join(AGENT_PROJECT_DIR, "auto_test")
SESSION_RECORDS_FILE = os.path.join(test_cases_dir, "session_records.json")


# 函数用于从文件中加载会话记录
def load_session_records():
    try:
        with open(SESSION_RECORDS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# 函数用于将会话记录保存到文件
def save_session_records(records):
    with open(SESSION_RECORDS_FILE, "w") as f:
        json.dump(records, f, indent=4, ensure_ascii=False)

# Streamlit页面布局
st.title("Talk with Thought Agent")
st.caption("🚀 A Task-Oriented Conversational Agent powered by Thoughtworks")

# 初始化session_state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.ui_messages = []

# 初始化session_id
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# 显示所有消息
for message in st.session_state.ui_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 处理用户输入并获取响应
if user_input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.ui_messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # 调用Agent接口
    response = call_agent(st.session_state.session_id, user_input)

    # 解析响应
    answer = response.get("response", {}).get("answer", {})
    additional_messages = response.get("additional_info", {})
    message_type = answer.get("messageType", "")

    if message_type == "FORMAT_INTELLIGENT_EXEC":
        agent_message = answer.get("content", {})
        # 提取operateType和operateSlots
        operate_type = agent_message.get("operateType", "")
        operate_slots = agent_message.get("operateSlots", {})
        # 转换为Markdown内容
        markdown_message = f"**Operation Type:** {operate_type}\n\n"
        agent_message['state'] = additional_messages['state']
        for key, value in operate_slots.items():
            markdown_message += f"**{key.capitalize()}:** {value}\n"
        st.chat_message("assistant").markdown(markdown_message)
        st.session_state.ui_messages.append({"role": "assistant", "content": markdown_message})
        st.session_state.messages.append({"role": "assistant", "content": agent_message})
    elif message_type == "FORMAT_TEXT":
        content = answer.get("content", {})
        agent_message = content.get("text", "")
        
        # merge additional_messages keys to content
        for key, value in additional_messages.items():
            content[key] = value

        st.chat_message("assistant").write(agent_message)
        st.session_state.ui_messages.append({"role": "assistant", "content": agent_message})
        st.session_state.messages.append({"role": "assistant", "content": content})

# 如果会话记录不为空，显示保存按钮
if st.session_state.messages:
    if st.button("Save Session Records"):
        # 加载现有的会话记录
        session_records = load_session_records()
        # 将当前会话记录添加到列表中
        session_records.append(st.session_state.messages)
        # 保存会话记录到文件
        save_session_records(session_records)
        st.success("Session records saved successfully!")
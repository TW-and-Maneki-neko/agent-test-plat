import streamlit as st
import requests
import uuid  # 导入uuid模块

from config import AGENT_API_URL

# 定义一个函数来调用Agent接口
def call_agent(session_id, user_input):
    payload = {
        "session_id": session_id,
        "user_input": user_input
    }
    response = requests.post(AGENT_API_URL, json=payload)
    return response.json()

# Streamlit页面布局
st.title("Talk with Thought Agent")
st.caption("🚀 A Task-Oriented Conversational Agent powered by Thoughtworks")

# 初始化session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

# 初始化session_id
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())  # 生成一个唯一的session_id

# 显示所有消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 处理用户输入并获取响应
if user_input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)
    
    # 调用Agent接口
    response = call_agent(st.session_state.session_id, user_input)

    # 解析响应
    answer = response.get("response", {}).get("answer", {})
    additional_messages = response.get("additional_info", [])
    message_type = answer.get("messageType", "")
    
    if message_type == "FORMAT_INTELLIGENT_EXEC":
        agent_message = answer.get("content", {})
        
        # 提取operateType和operateSlots
        operate_type = agent_message.get("operateType", "")
        operate_slots = agent_message.get("operateSlots", {})
        
        # 转换为Markdown内容
        markdown_message = f"**Operation Type:** {operate_type}\n\n"
        for key, value in operate_slots.items():
            markdown_message += f"**{key.capitalize()}:** {value}\n"
        
        st.chat_message("assistant").markdown(markdown_message)
    elif message_type == "FORMAT_TEXT":
        content = answer.get("content", {})
        agent_message = content.get("text", "")
        st.chat_message("assistant").write(agent_message)
    else:
        agent_message = "对不起，我不明白您的意思。"
        st.chat_message("assistant").write(agent_message)

    # 显示Agent的响应
    st.session_state.messages.append({"role": "assistant", "content": markdown_message if message_type == "FORMAT_INTELLIGENT_EXEC" else agent_message})

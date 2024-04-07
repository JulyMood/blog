import streamlit as st
from view.sidebar import sidebar
from app.services.rag_service import rag_chat

# 加载侧边栏
sidebar()

if "messages" not in st.session_state:
    st.session_state.messages = []

# 加载聊天记录
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 输入框
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        # 流式打印生成结果
        response = st.write_stream(rag_chat(prompt))
    st.session_state.messages.append({"role": "assistant", "content": response})

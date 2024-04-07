import json
import re

import streamlit as st

from app.services import user_service
from view.encrypted_cookie_manager import EncryptedCookieManager


def user_load(cookies):
    c1, c2 = st.columns(2)
    with c1.popover('登录'):
        with st.form('登录'):
            username = st.text_input("用户名")
            password = st.text_input("密码", type="password")
            submitted = st.form_submit_button("提交")
            if submitted:
                token = user_service.login(username, password)
                if token:
                    st.success('登录成功')
                    cookies.update({'token': token})
                    st.experimental_rerun()
                else:
                    st.error('用户名密码错误')
    with c2.popover('注册'):
        with st.form('注册'):
            email = st.text_input("邮箱")
            username = st.text_input("用户名")
            password = st.text_input("密码", type="password")
            password_2 = st.text_input("再次密码", type="password")
            submitted = st.form_submit_button("提交")
            if submitted:
                if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
                    st.error('邮箱输入有误')
                    return
                if password != password_2:
                    st.error('两次密码不一致')
                    return
                result = user_service.register(email, username, password)
                if result is True:
                    st.success('注册成功')
                else:
                    st.error('注册失败,' + result)


def sidebar():
    with open('view/css/style.css') as css:
        st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)
    with st.sidebar:
        cookies = EncryptedCookieManager(password='dmas1vdsak3d1xpqw0zzd8')
        if not cookies.ready():
            st.stop()
        if cookies.get('token'):
            userinfo = user_service.check_token(cookies.get('token'))
            if userinfo:
                userinfo = json.loads(userinfo)
                st.session_state.update(
                    {'username': userinfo['username'], 'role': userinfo['role'], 'user_id': userinfo['id']})
                col1, col2 = st.columns([1, 3])
                if col1.button('登出'):
                    cookies.pop('token')
                    st.session_state.pop('username')
                    st.session_state.pop('role')
                    st.session_state.pop('user_id')
                    st.experimental_rerun()
                msg = (
                    f'<span style="color: #0bb2ea; font-size: 20px;">:tada: **{st.session_state["username"]}**</span>'
                    f'<span style="color: gray; font-size: 14px;"> _[{st.session_state["role"]}]_</span>')
                col2.markdown(msg, unsafe_allow_html=True)
            else:
                user_load(cookies)
        else:
            user_load(cookies)
        st.markdown('---')
        st.page_link('home.py', label='主页', icon='🏠')
        st.page_link('pages/article.py', label='文章', icon='📖')
        st.page_link('pages/live.py', label='相册', icon='📷')
        st.page_link('pages/link.py', label='链接', icon='🔗')
        st.page_link('pages/chatbot.py', label='聊天', icon='🤖️')


def page_widget(total_pages, state_key):
    # 每行可容纳的页码
    row_index = 20
    num_rows = (total_pages + row_index - 1) // row_index

    for row in range(num_rows):
        with st.container():
            col = st.columns(row_index)
            for index in range(row * row_index, min((row + 1) * row_index, total_pages)):
                button_label = str(index + 1)

                # 使用闭包来避免延迟绑定问题
                def on_click(index=index + 1):
                    def callback():
                        st.session_state.update({state_key: index})

                    return callback

                col[index % row_index].button(button_label, on_click=on_click())

import base64
from view.sidebar import sidebar
import streamlit as st
from streamlit_modal import Modal
from app.dao import live
from view.timeline import timeline


st.set_page_config(page_title="Timeline", layout="wide")


def publish(modal):
    with modal.container():
        with st.form('发表'):
            caption = st.text_input('图片标题', max_chars=50).strip()
            media = st.file_uploader('上传图片', type=['png', 'jpg', 'jpeg'])
            if media is not None:
                file_bytes = media.read()
                base64_encoded = base64.b64encode(file_bytes).decode("utf-8")
                base64_media = f"data:;base64,{base64_encoded}"
            content = st.text_input("文字内容", max_chars=500).strip()
            submitted = st.form_submit_button("提交")
            if submitted:
                if not caption or not content or not caption or not base64_media:
                    st.error('输入不能为空')
                    return
                result = live.create_live(content, base64_media, caption)
                if result is True:
                    st.success('发布成功')
                    modal.close()
                else:
                    st.error('发布失败，请检查数据\n' + result)


sidebar()

modal_create = Modal('动态', key='live_create', padding=5)

if st.session_state.get('role') == 'admin':
    if modal_create.is_open():
        publish(modal_create)
    if st.button('发布动态'):
        modal_create.open()

live_list = live.query()
events = []
for live in live_list:
    events.append({
        'media': {'url': live.media_url, 'caption': live.caption},
        'start_date': {'year': live.create_time.year, 'month': live.create_time.month, 'day': live.create_time.day},
        'text': {'headline': live.caption, 'text': live.content}
    })

time_line_data = {
    'title': {"media": {
        "url": "https://img1.baidu.com/it/u=1469793249,2277921754&fm=253&fmt=auto&app=120&f=JPEG?w=1229&h=800",
        "caption": "",
        "credit": ""
    },
        "text": {
            "headline": "欢迎观看",
            "text": "<p>我的时间轴</p>"
        }
    },
    'events': events
}

timeline(time_line_data, height=600)

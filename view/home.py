import streamlit as st
from app.services import article_service
from view.sidebar import sidebar
# 加载侧边栏
sidebar()
st.markdown('![Release Notes](https://img.shields.io/github/release/langchain-ai/langchain)')

col = st.columns([4, 1])
col[0].header(f'🌲某棵的个人空间')
col[1].image('view/images/GitHub-Mark.png', width=40)
st.subheader('', divider='rainbow')
st.caption('这里是我分享我的想法、学习和探索的地方。')

time_group, type_group = article_service.statistics()
if time_group is not None:
    g1, g2 = st.columns(2)
    g1.write('文章发布统计')
    g1.line_chart(time_group, use_container_width=True)
    g2.write('文章类型统计')
    g2.bar_chart(type_group)


st.subheader('推荐阅读')
article_list = article_service.get_recommendation()
for article in article_list:
    with st.expander(f'_[{article.type}]_ &nbsp;&nbsp;&nbsp; **{article.title}**'):
        st.write(article.content)

st.caption('如果你想联系我，请发送邮件到 takeitcooloo@gmail.com，或者在社交媒体上关注我。')

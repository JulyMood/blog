from view.sidebar import sidebar, page_widget
import streamlit as st
from streamlit_modal import Modal
from app.services import article_service


def publish(modal):
    with modal.container():
        with st.form('发表'):
            title = st.text_input("标题", max_chars=100, value=st.session_state[
                'article_update'].title if modal.key == 'article_update' else '')
            type = st.text_input("文章类型", max_chars=10, value=st.session_state[
                'article_update'].type if modal.key == 'article_update' else '').strip()
            content = st.text_area('文章内容(支持markdown格式)', value=st.session_state[
                'article_update'].content if modal.key == 'article_update' else '').strip()
            submitted = st.form_submit_button("提交")
            if submitted:
                if not title or not type or not content:
                    st.error('内容不能为空')
                    return
                if modal.key == 'article_create':
                    result = article_service.create_article(title, type, content)
                else:
                    result = article_service.update_article(st.session_state['article_update'].id, title, type, content)
                if result is True:
                    st.success('发布成功')
                    modal.close()
                else:
                    st.error('发布失败，请检查数据\n' + result)


sidebar()

modal_create = Modal('发布', key='article_create', padding=5)
modal_update = Modal('修改', key='article_update', padding=5)
comments_modal = Modal('评论', key='comments_modal', padding=5)

if st.session_state.get('role') == 'admin':
    if modal_create.is_open():
        publish(modal_create)
    if modal_update.is_open():
        publish(modal_update)
    if comments_modal.is_open():
        publish(comments_modal)
    if st.button('发表文章'):
        modal_create.open()

current_page = st.session_state.get('article_current_page', 1)
article_list, total_pages = article_service.query_article(current_page)
for article in article_list:
    with st.expander(f'_[{article.type}]_ &nbsp;&nbsp;&nbsp; **{article.title}**'):
        col = st.columns([4, 2, 3, 10])
        col[0].markdown(f'<span style="color: green;">*{article.create_time}*</span>', unsafe_allow_html=True)
        if st.session_state.get('role') == 'admin':
            if col[1].button('修改', key=f'article_update_{article.id}'):
                st.session_state['article_update'] = article
                modal_update.open()
            with col[2].popover('删除'):
                st.write(f'是否确认删除: **{article.title}**')


                def on_click(_id=article.id):
                    def callback():
                        article_service.delete_article(_id)

                    return callback


                st.button('确认', key=f'article_del_{article.id}', on_click=on_click())
        st.markdown(article.content, unsafe_allow_html=True)


        def likes(_id=article.id):
            def callback():
                article_service.like_article(_id)

            return callback


        bottom = st.columns([1, 1, 6])
        bottom[0].button(f':+1: &nbsp; {article.like_count}', key=f'article_up_{article.id}', on_click=likes())


        def sub_comments(_id=article.id):
            def callback():
                comment = st.session_state[f'comment_{_id}']
                if comment:
                    article_service.add_comments(st.session_state.get('user_id'),
                                                 st.session_state.get('username', '匿名用户'), _id, comment)

            return callback


        if bottom[1].button(':speech_balloon:', key=f'comments_{article.id}'):
            comment = st.text_input('评论', key=f'comment_{article.id}').strip()
            st.button('提交', key=f'comments_sub_{article.id}', on_click=sub_comments())

        with st.container(border=True):
            for x in article.comments[::-1]:
                col = st.columns([1, 1, 2])
                col[0].markdown(f'<span style="color: green; font-size: 13px;">*{x.create_time}*</span>',
                                unsafe_allow_html=True)
                col[1].markdown(f'<span style="color: #0bb2ea; font-size: 13px;">*{x.username}*</span>',
                                unsafe_allow_html=True)
                if st.session_state.get('user_id') is not None and (
                        x.user_id == st.session_state.get('user_id') or st.session_state.get('role') == 'admin'):
                    with col[2].popover('删除'):
                        st.write(f'是否确认删除评论')


                        def on_click(_id=x.id):
                            def callback():
                                article_service.del_comments(_id)

                            return callback


                        st.button('确认', key=f'comment_del_{x.id}', on_click=on_click())
                st.markdown(x.content)

page_widget(total_pages, 'article_current_page')

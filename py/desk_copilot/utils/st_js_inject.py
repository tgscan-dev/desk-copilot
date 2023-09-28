import html
import uuid

import streamlit as st


def exec_js(source: str) -> None:
    div_id = uuid.uuid4()

    st.markdown(
        f"""
    <div style="display:none" id="{div_id}">
        <iframe src="javascript: \
            var script = document.createElement('script'); \
            script.type = 'text/javascript'; \
            script.text = {html.escape(repr(source))}; \
            var div = window.parent.document.getElementById('{div_id}'); \
            div.appendChild(script); \
            div.parentElement.parentElement.parentElement.style.display = 'none'; \
        "/>
    </div>
    """,
        unsafe_allow_html=True,
    )

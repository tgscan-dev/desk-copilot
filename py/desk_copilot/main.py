import streamlit as st
from desk_copilot.agent import get_agent, msgs
from desk_copilot.utils import get_kv_store
from desk_copilot.utils.st_js_inject import exec_js
from langchain.callbacks import StreamlitCallbackHandler
from toolz import memoize

conf = get_kv_store("conf.json")
st.set_page_config(initial_sidebar_state="collapsed")


exec_js(
    """
document.querySelector('div[data-testid="stToolbar"]').style.display='none';
document.querySelector('footer').style.display='none';
"""
)
model_name = "gpt-4"
with st.sidebar:
    openai_api_key = (
        st.text_input(
            "OpenAI API Key", type="password", value=conf.get("openai_api_key")
        )
        if conf.get("openai_api_key") is not None
        else st.text_input("OpenAI API Key", type="password")
    )
    if openai_api_key:
        st.info("OpenAI API Key set")
        conf.set("openai_api_key", openai_api_key)
    model_name = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4"], index=1)
if not openai_api_key:
    st.info("Enter an OpenAI API Key to continue")
    if button := st.button("Input API Key"):
        exec_js(
            """document.querySelector("div[data-testid='collapsedControl'] button").click()"""
        )
    st.stop()

agent = get_agent(openai_api_key, model_name)

print("agent initialized")

for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)


@memoize
def get_st_callback(ctn):
    return StreamlitCallbackHandler(ctn)


if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        container = st.container()

        response = agent.run(prompt, callbacks=[get_st_callback(container)])
        st.write(response)

import langchain
from desk_copilot.prompt.system_prompt import SYSTEM_PROMPT
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory, StreamlitChatMessageHistory
from langchain.prompts import MessagesPlaceholder
from langchain.schema import SystemMessage
from langchain.tools import DuckDuckGoSearchRun, PythonREPLTool, ShellTool
from toolz import memoize

langchain.debug = True

msgs = StreamlitChatMessageHistory(key="memory")


@memoize
def get_agent(openai_api_key, model_name):
    print(model_name)
    llm = ChatOpenAI(
        temperature=0, model=model_name, streaming=True, openai_api_key=openai_api_key
    )
    tools = [PythonREPLTool(), ShellTool(), DuckDuckGoSearchRun()]
    memory = ConversationBufferWindowMemory(
        chat_memory=msgs, memory_key="memory", return_messages=True, k=8
    )
    return initialize_agent(
        tools,
        llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        agent_kwargs={
            "system_message": SystemMessage(content=SYSTEM_PROMPT),
            "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
        },
        memory=memory,
        handle_parsing_errors=True,
        verbose=True,
    )

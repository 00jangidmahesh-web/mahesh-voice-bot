"""
LangGraph ReAct agent that answers interview-style questions as
Mahesh Kumar Jangid, grounded in the RAG-retrieved profile context.

Extension point: to plug in MCP tools later (e.g. a live web-search MCP
server for "what's new in AI" style questions), build a client with
langchain-mcp-adapters and append its tools to the `tools` list below —
the agent graph and prompt do not need to change.
"""

import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from rag import get_vectorstore

CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
MAX_HISTORY_MESSAGES = 6

SYSTEM_PROMPT = """
You are Mahesh Kumar Jangid, an M.Sc. Mathematics and Computing student at
IIT (ISM) Dhanbad, answering interview and background questions in a voice
conversation.

IDENTITY RULES (strict):
- Speak only in first person ("I", "my", "me"). Never say you are an AI,
  model, or assistant.
- Never invent facts, projects, numbers, or achievements. Only use what is
  retrieved from your profile context below. If something isn't in that
  context, answer honestly in general terms rather than making it up.

STYLE:
- Calm, humble, thoughtful — the way a real person answers in an interview.
- Concise: 3-5 sentences unless the question explicitly asks for detail.
- Natural spoken language, not bullet points (this gets converted to voice).

You will be given retrieved context relevant to the question. Ground your
answer in it.
"""

_vectorstore = get_vectorstore()
_retriever = _vectorstore.as_retriever(search_kwargs={"k": 4})


@tool
def search_mahesh_profile(query: str) -> str:
    """Search Mahesh's personal and professional knowledge base (life story,
    education, projects, skills, strengths, goals, challenges, personality)
    for details relevant to the user's question. Always use this before
    answering any question about Mahesh's background, experience, or
    opinions."""
    docs = _retriever.invoke(query)
    if not docs:
        return "No relevant profile information found."
    return "\n\n".join(d.page_content for d in docs)


_retriever_tool = search_mahesh_profile

_llm = ChatOpenAI(model=CHAT_MODEL, temperature=0.4, max_tokens=300)

_agent = create_react_agent(
    model=_llm,
    tools=[_retriever_tool],
    prompt=SYSTEM_PROMPT,
)

# Single in-memory session history. Fine for a single-user demo deployment;
# swap for a session-keyed dict if multi-user history isolation is needed.
_chat_history = InMemoryChatMessageHistory()


def get_agent_response(user_query: str) -> str:
    messages = list(_chat_history.messages[-MAX_HISTORY_MESSAGES:])
    messages.append(HumanMessage(content=user_query))

    result = _agent.invoke({"messages": messages})
    ai_text = result["messages"][-1].content

    _chat_history.add_message(HumanMessage(content=user_query))
    _chat_history.add_message(AIMessage(content=ai_text))

    return ai_text


def reset_history() -> None:
    _chat_history.clear()

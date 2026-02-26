from typing import Annotated, List, TypedDict, Optional
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage, SystemMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

def get_llm(tools_list=None):
    # Инициализируем Ollama. Модель qwen2.5:7b отлично справляется с JSON и инструментами.
    llm = ChatOllama(
        model="qwen2.5:7b",
        temperature=0, # Убираем случайность для стабильного вызова инструментов
        base_url="http://localhost:11434" # Стандартный адрес Ollama [5]
    )

    # Привязываем инструменты, чтобы модель "видела" свои возможности
    if tools_list:
        return llm.bind_tools(tools_list)
    return llm

async def call_model(state: AgentState, config: Optional[RunnableConfig] = None):
    """Узел агента, который теперь работает асинхронно."""
    prompt = SystemMessage(content=(
        "Ты — Agentic Dependency Updater. Твоя цель — анализировать зависимости. "
        "ОБЯЗАТЕЛЬНО используй инструменты для действий. Никогда не пиши советы текстом."
    ))
    messages = [prompt] + state["messages"]

    # Извлекаем инструменты из конфигурации
    tools = config.get("configurable", {}).get("tools", []) if config else []
    llm = get_llm(tools_list=tools)

    # Ollama поддерживает ainvoke, поэтому возвращаем await
    response = await llm.ainvoke(messages)
    return {"messages": [response]}

def create_agent_graph(tools_list):
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(tools_list))
    workflow.add_edge(START, "agent")

    def should_continue(state: AgentState):
        last_message = state["messages"][-1]
        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            return "tools"
        return END

    workflow.add_conditional_edges("agent", should_continue)
    workflow.add_edge("tools", "agent")
    return workflow.compile()
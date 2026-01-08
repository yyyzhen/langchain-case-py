"""
02 - 消息裁剪示例
使用 middleware 裁剪消息，控制上下文长度
"""
import asyncio
from typing import Any
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_model
from langchain.messages import HumanMessage, AIMessage, ToolMessage, RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langgraph.runtime import Runtime
from src.base_model import model
from src.utils import print_agent_response

@before_model
def trim_middleware(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """
    消息裁剪中间件
    通过修改 max_tokens 可以控制保留的消息数量
    """
    messages = state["messages"]
    
    # 如果消息数量小于等于3，不需要裁剪
    if len(messages) <= 3:
        return None
    
    # 保留第一条消息和最近的消息
    first_msg = messages[0]
    recent_messages = messages[-3:] if len(messages) % 2 == 0 else messages[-4:]
    new_messages = [first_msg] + recent_messages
    
    return {
        "messages": [
            RemoveMessage(id=REMOVE_ALL_MESSAGES),
            *new_messages
        ]
    }


async def main():
    # 创建 Agent
    agent = create_agent(
        model=model,
        middleware=[trim_middleware],
        system_prompt="你是一个乐于助人的AI助手。",
    )

    # 构造模拟的历史消息
    history = [
        # 这两条消息会被裁剪掉
        HumanMessage(content="你好，我是小明", id="msg_1"),
        AIMessage(content="你好小明！", id="msg_2"),
        # 这里的消息会保留
        HumanMessage(content="南极天气如何？", id="msg_3"),
        AIMessage(
            content="",
            id="msg_4",
            tool_calls=[{"id": "call_123", "name": "get_weather", "args": {"location": "Antarctica"}}]
        ),
        ToolMessage(
            tool_call_id="call_123",
            content="南极大陆天气晴朗，气温 -30度",
            name="get_weather",
            id="msg_5"
        ),
    ]

    # 调用 Agent
    response = await agent.ainvoke({"messages": history})
    print_agent_response(response)


if __name__ == "__main__":
    asyncio.run(main())


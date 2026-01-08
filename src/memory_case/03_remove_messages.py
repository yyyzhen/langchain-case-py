"""
03 - 消息删除示例
使用 RemoveMessage 标记要删除的消息
"""
import asyncio
from typing import Any
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_model
from langchain.messages import HumanMessage, AIMessage, RemoveMessage
from langgraph.runtime import Runtime
from src.base_model import model
from src.utils import print_agent_response

@before_model
def remove_message_middleware(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """
    自动移除多余消息的中间件
    当消息数量超过4条时，删除最前面的2条消息
    """
    messages = state["messages"]
    msg_len = len(messages)
    
    if msg_len > 4:
        # RemoveMessage 标记要删除的消息
        return {
            "messages": [
                RemoveMessage(id=msg.id) 
                for msg in messages[:2] 
                if msg.id
            ]
        }
    return None


async def main():
    # 创建 Agent
    agent = create_agent(
        model=model,
        middleware=[remove_message_middleware],
        system_prompt="你是一个助手，简短回答用户问题。",
    )

    # 构造历史消息
    history = [
        # 第一轮对话
        HumanMessage(content="北京今天天气怎么样？", id="msg_weather"),
        AIMessage(content="今天北京天气晴朗，气温20度", id="msg_weather_answer"),
        # 第二轮对话
        HumanMessage(content="推荐附近的餐厅", id="msg_restaurant"),
        AIMessage(content="好的，我推荐你附近的餐厅是：海底捞", id="msg_restaurant_answer"),
    ]

    # 第三轮对话，需要删除最前面两轮对话的消息
    response = await agent.ainvoke({
        "messages": [
            *history,
            HumanMessage(content="刚才我问了什么问题？", id="msg_question"),
        ]
    })

    print_agent_response(response)


if __name__ == "__main__":
    asyncio.run(main())


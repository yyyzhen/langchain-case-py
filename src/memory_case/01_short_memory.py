"""
01 - 短期记忆示例
使用 InMemorySaver 作为检查点工具实现对话记忆
"""
import asyncio
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from src.base_model import model
from src.utils import print_agent_response


# 使用内存保存器做为检查点工具
checkpointer = InMemorySaver()


@tool
def get_weather(city: str) -> str:
    """获取某地的天气信息"""
    return f"城市: {city} 的天气是晴天"


@tool  
def get_user_location() -> str:
    """获取用户位置"""
    return "用户位置: 海拉鲁大陆"


async def main():
    # 创建 Agent，设置检查点
    agent = create_agent(
        model=model,
        tools=[get_weather, get_user_location],
        checkpointer=checkpointer
    )

    # 第一次调用，设置线程ID
    response1 = await agent.ainvoke(
        {"messages": [HumanMessage(content="外面的天气怎么样")]},
        config={"configurable": {"thread_id": "1"}}
    )
    print("第一次对话:")
    print_agent_response(response1)

    # 第二次调用，使用相同的线程ID，可以获取到之前的对话历史
    response2 = await agent.ainvoke(
        {"messages": [HumanMessage(content="哪里的天气是晴天")]},
        config={"configurable": {"thread_id": "1"}}
    )
    print("\n第二次对话 (记住了之前的上下文):")
    print_agent_response(response2)


if __name__ == "__main__":
    asyncio.run(main())


"""
06 - checkpoints 流式模式示例
使用 stream_mode="checkpoints" 获取检查点信息
"""
import asyncio
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from src.base_model import model


# 创建内存保存器
checkpointer = InMemorySaver()


@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    return f"城市: {city} 的天气是晴天!"


async def main():
    # 创建 Agent，设置检查点
    agent = create_agent(
        model=model,
        tools=[get_weather],
        checkpointer=checkpointer,
    )

    # 使用 stream 方法，设置 stream_mode="checkpoints"
    async for checkpoint in agent.astream(
        {"messages": [{"role": "user", "content": "杭州的天气怎么样"}]},
        config={"configurable": {"thread_id": "1"}},
        stream_mode="checkpoints",
    ):
        print("步骤:", checkpoint.get("metadata", {}).get("step"))
        print("当前状态:", checkpoint.get("values"))
        print("下一步节点:", checkpoint.get("next"))
        print("任务详情:", checkpoint.get("tasks"))
        print("---")


if __name__ == "__main__":
    asyncio.run(main())

"""
输出示例:
步骤: -1
当前状态: {'messages': []}
下一步节点: ['__start__']
任务详情: [{'id': '...', 'name': '__start__', ...}]
---
步骤: 0
当前状态: {
  'messages': [HumanMessage(content='杭州的天气怎么样', ...)]
}
下一步节点: ['model_request']
任务详情: [{'id': '...', 'name': 'model_request', ...}]
---
......
"""


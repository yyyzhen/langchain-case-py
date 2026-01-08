"""
07 - tasks 流式模式示例
使用 stream_mode="tasks" 获取任务执行信息
"""
import asyncio
from langchain.agents import create_agent
from langchain.tools import tool
from src.base_model import model


@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    return f"城市: {city} 的天气是晴天!"


async def main():
    # 创建 Agent
    agent = create_agent(
        model=model,
        tools=[get_weather],
    )

    # 使用 stream 方法，设置 stream_mode="tasks"
    async for task in agent.astream(
        {"messages": [{"role": "user", "content": "杭州的天气怎么样"}]},
        stream_mode="tasks",
    ):
        if "input" in task:
            print(f"任务开始: {task.get('name')}")
            print(f"输入: {task.get('input')}")
            print(f"触发器: {task.get('triggers')}")
        elif "result" in task:
            print(f"任务完成: {task.get('name')}")
            print(f"结果: {task.get('result')}")
        print("---")


if __name__ == "__main__":
    asyncio.run(main())

"""
输出示例:
任务开始: model_request
输入: {'messages': [HumanMessage(content='杭州的天气怎么样')]}
触发器: ['branch:to:model_request']
---
任务完成: model_request
结果: {'messages': [AIMessage(tool_calls=[...])]}
---
任务开始: tools
输入: {'messages': [...]}
触发器: ['branch:to:model_request']
---
任务完成: tools
结果: {'messages': [ToolMessage(content='城市: 杭州的天气是晴天!')]}
---
"""


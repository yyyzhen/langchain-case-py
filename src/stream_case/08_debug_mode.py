"""
08 - debug 流式模式示例
使用 stream_mode="debug" 获取详细调试信息
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

    # 使用 stream 方法，设置 stream_mode="debug"
    async for chunk in agent.astream(
        {"messages": [{"role": "user", "content": "杭州的天气怎么样"}]},
        stream_mode="debug",
    ):
        print("调试信息:", chunk)


if __name__ == "__main__":
    asyncio.run(main())

"""
输出示例:
{
  'step': 1,
  'type': 'task',
  'timestamp': '2025-11-23T08:52:11.532Z',
  'payload': {
    'id': '...',
    'name': 'model_request',
    'input': {'messages': [...]},
    'triggers': ['branch:to:model_request'],
    'interrupts': []
  }
}

{
  'step': 1,
  'type': 'task_result',
  'timestamp': '2025-11-23T08:52:13.149Z',
  'payload': {
    'id': '...',
    'name': 'model_request',
    'result': {'messages': [...]},
    'interrupts': []
  }
}

{'step': 2, 'type': 'task', 'payload': {...}}
{'step': 2, 'type': 'task_result', 'payload': {...}}
"""


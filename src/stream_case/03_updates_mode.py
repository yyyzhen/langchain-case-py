"""
03 - updates 流式模式示例
使用 stream_mode="updates" 获取每一步的增量更新
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

    # 使用 stream 方法，设置 stream_mode="updates"
    async for chunk in agent.astream(
        {"messages": [{"role": "user", "content": "杭州的天气怎么样"}]},
        stream_mode="updates"
    ):
        print("更新:", chunk)


if __name__ == "__main__":
    asyncio.run(main())

"""
输出示例:
{
  'model_request': {
    'messages': [AIMessage(调用工具get_weather...)]
  }
}

{
  'tools': {
    'messages': [ToolMessage(城市: 杭州 的天气是晴天!)]
  }
}

{
  'model_request': {
    'messages': [AIMessage(杭州的天气是晴天，建议...)]
  }
}
"""


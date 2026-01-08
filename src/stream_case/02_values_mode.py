"""
02 - values 流式模式示例
使用 stream_mode="values" 获取每一步的完整状态
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

    # 使用 stream 方法，设置 stream_mode="values"
    async for chunk in agent.astream(
        {"messages": [{"role": "user", "content": "杭州的天气怎么样"}]},
        stream_mode="values"
    ):
        print("当前状态消息数量:", len(chunk.get("messages", [])))
        for msg in chunk.get("messages", []):
            print(f"  [{type(msg).__name__}]: {str(msg.content)[:50]}...")


if __name__ == "__main__":
    asyncio.run(main())

"""
输出示例:
当前状态消息数量: 1
  [HumanMessage]: 杭州的天气怎么样...

当前状态消息数量: 2
  [HumanMessage]: 杭州的天气怎么样...
  [AIMessage]: (调用工具 get_weather)...

当前状态消息数量: 4
  [HumanMessage]: 杭州的天气怎么样...
  [AIMessage]: (调用工具 get_weather)...
  [ToolMessage]: 城市: 杭州 的天气是晴天!...
  [AIMessage]: 杭州的天气是晴天...
"""


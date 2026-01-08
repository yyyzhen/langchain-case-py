"""
04 - custom 流式模式示例
使用 stream_mode="custom" 获取自定义数据
"""
import asyncio
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.config import get_stream_writer
from src.base_model import model


@tool
async def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    # 获取流写入器
    writer = get_stream_writer()
    
    # 将数据写入流中
    writer(f"正在获取城市: {city} 的数据")
    
    # 假装获取数据需要1秒
    await asyncio.sleep(1)
    
    # 将数据写入流中
    writer(f"获取城市: {city} 的数据完成")
    
    return f"城市: {city} 的天气是晴天!"


async def main():
    # 创建 Agent
    agent = create_agent(
        model=model,
        tools=[get_weather],
    )

    # 使用 stream 方法，设置 stream_mode="custom"
    async for chunk in agent.astream(
        {"messages": [{"role": "user", "content": "杭州的天气怎么样"}]},
        stream_mode="custom"
    ):
        print("自定义数据:", chunk)


if __name__ == "__main__":
    asyncio.run(main())

"""
输出示例:
自定义数据: 正在获取城市: 杭州 的数据

(等待一秒)

自定义数据: 获取城市: 杭州 的数据完成
"""


"""
05 - 多流式模式示例
同时使用多个 stream_mode
"""
import asyncio
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from src.base_model import model


async def main():
    # 创建 Agent
    agent = create_agent(
        model=model,
        tools=[],
        system_prompt="你是一位小学语文老师。",
    )

    # 使用 stream 方法，设置多个 stream_mode
    async for mode, chunk in agent.astream(
        {"messages": [HumanMessage(content="小明今天为什么没有来上学？")]},
        stream_mode=["messages", "values"],
    ):
        if mode == "messages":
            message_chunk, metadata = chunk
            if message_chunk.text:
                print(f"[messages] {message_chunk.text}")
        elif mode == "values":
            print(f"[values] 消息数量: {len(chunk.get('messages', []))}")


if __name__ == "__main__":
    asyncio.run(main())

"""
输出示例:
[messages] 哎
[messages] 呀
[messages] ,小
[messages] 明今天没
...
[values] 消息数量: 2
"""


"""
01 - messages 流式模式示例
使用 stream_mode="messages" 流式获取 LLM token
"""
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from src.base_model import model


def main():
    # 创建 Agent
    agent = create_agent(
        model=model,
        tools=[],
        system_prompt="你是一位小学语文老师。",
    )

    # 使用 stream 方法，设置 stream_mode="messages"
    for message_chunk, metadata in agent.stream(
        {"messages": [HumanMessage(content="小明今天为什么没有来上学？")]},
        stream_mode="messages",
    ):
        # 每个 chunk 包含一个 AIMessageChunk 和元数据
        if message_chunk.text:
            print(message_chunk.text, end="", flush=True)

    print()  # 换行


if __name__ == "__main__":
    main()

"""
流式输出示例:
哎呀,小明今天没有来上学...
(逐字输出，直到响应结束)
"""


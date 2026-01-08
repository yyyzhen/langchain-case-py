"""
03 - AIMessage 示例
AIMessage 是模型返回的消息，通常由模型自动生成
这里我们展示如何使用模型获取 AIMessage，以及 AIMessage 的结构
"""
import asyncio
from langchain.messages import SystemMessage
from src.base_model import model
import time


async def main():
    # 创建系统消息
    msg1 = SystemMessage(
        content="你是一个电影推荐专家，请根据用户的问题推荐电影",
        id="123",
        name="movie-expert",
        response_metadata={
            "custom_field": "我是自定义的元数据",
            "created_at": int(time.time() * 1000)
        }
    )

    # 调用模型，获取 AIMessage
    result = await model.ainvoke([
        msg1,
        {"role": "user", "content": "请推荐一部科幻电影"}
    ])

    print("AIMessage 对象:")
    print(result)
    print("\nAIMessage 内容:")
    print(result.text)


if __name__ == "__main__":
    asyncio.run(main())

"""
模型响应内容示例:
AIMessage {
  "id": "chatcmpl-xxx",
  "content": "当然！我推荐你观看《银翼杀手2049》...",
  "additional_kwargs": {},
  "response_metadata": {
    "token_usage": {
      "prompt_tokens": 28,
      "completion_tokens": 209,
      "total_tokens": 237
    },
    "finish_reason": "stop",
    "model_name": "qwen3-max"
  },
  "tool_calls": [],
  "usage_metadata": {
    "output_tokens": 209,
    "input_tokens": 28,
    "total_tokens": 237
  }
}
"""


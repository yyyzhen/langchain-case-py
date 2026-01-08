"""
01 - SystemMessage 示例
SystemMessage 用于设置 AI 助手的角色和行为指南
"""
from langchain.messages import SystemMessage
import time

# 简单创建 SystemMessage
msg1 = SystemMessage(content='你是一个电影推荐专家，请根据用户的问题推荐电影')
print("简单 SystemMessage:")
print(msg1)

"""
输出:
SystemMessage {
  "content": "你是一个电影推荐专家，请根据用户的问题推荐电影",
  "additional_kwargs": {},
  "response_metadata": {}
}
"""

# 带有更多参数的 SystemMessage
msg2 = SystemMessage(
    # 消息内容，必填
    content="你是一个电影推荐专家，请根据用户的问题推荐电影",
    # 消息id，可以用来标识消息，方便后续检索
    id="123",
    # 消息名称，可以用来标识消息，方便后续检索
    name="movie-expert",
    # 响应元数据，可以用来存储一些额外的信息
    response_metadata={
        "custom_field": "我是自定义的元数据",
        "created_at": int(time.time() * 1000)
    }
)
print("\n带参数的 SystemMessage:")
print(msg2)

"""
输出:
SystemMessage {
  "id": "123",
  "content": "你是一个电影推荐专家，请根据用户的问题推荐电影",
  "name": "movie-expert",
  "additional_kwargs": {},
  "response_metadata": {
    "custom_field": "我是自定义的元数据",
    "created_at": 1762179460040
  }
}
"""


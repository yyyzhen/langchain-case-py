"""
02 - HumanMessage 示例
HumanMessage 用于表示用户发送的消息
"""
from langchain.messages import HumanMessage
import time

# 简单创建 HumanMessage
msg1 = HumanMessage(content='请推荐一部电影')
print("简单 HumanMessage:")
print(msg1)

"""
输出:
HumanMessage {
  "content": "请推荐一部电影",
  "additional_kwargs": {},
  "response_metadata": {}
}
"""

# 带有更多参数的 HumanMessage
msg2 = HumanMessage(
    content='请推荐一部电影',
    id='123',
    name='movie-expert',
    response_metadata={
        'custom_field': '我是自定义的元数据',
        'created_at': int(time.time() * 1000)
    }
)
print("\n带参数的 HumanMessage:")
print(msg2)

"""
输出:
HumanMessage {
  "id": "123",
  "content": "请推荐一部电影",
  "name": "movie-expert",
  "additional_kwargs": {},
  "response_metadata": {
    "custom_field": "我是自定义的元数据",
    "created_at": 1762179429992
  }
}
"""


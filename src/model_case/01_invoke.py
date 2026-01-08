"""
01 - invoke 方法示例
invoke 方法会返回完整的响应，需要等待模型生成完成
"""
from src.base_model import model


def main():
    # invoke 方法会返回一个 AIMessage 对象
    result = model.invoke("你是谁？")
    print('langchain 格式化结果：', result.text)
    print('完整消息对象：', result)


if __name__ == "__main__":
    main()

"""
模型直接输出内容示例:
AIMessage {
  "id": "chatcmpl-xxx",
  "content": "我是通义千问（Qwen），由通义实验室研发的超大规模语言模型...",
  "response_metadata": {
    "token_usage": {...},
    "model_name": "qwen3-max",
    "finish_reason": "stop"
  }
}
"""


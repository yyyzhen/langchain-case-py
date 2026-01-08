"""
02 - stream 方法示例
stream 方法会返回一个异步迭代器，可以逐步获取模型响应
"""
from src.base_model import model


def main():
    # stream 方法返回一个异步迭代器
    print('langchain流式响应输出：')
    for chunk in model.stream("你是谁？"):
        # 每个 chunk 是一个 AIMessageChunk 对象
        print(chunk.text, end="", flush=True)
    print()  # 换行


if __name__ == "__main__":
    main()

"""
模型流式响应内容:
我是  # 第一个chunk
通义  # 第二个chunk
千问  # 第三个chunk
...   # 依次类推
"""


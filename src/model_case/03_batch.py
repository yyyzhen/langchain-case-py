"""
03 - batch 方法示例
batch 方法可以并行调用多个模型请求，返回一个列表
"""
from src.base_model import model


def main():
    # batch 方法可以并行调用多个模型，返回一个列表
    result = model.batch(
        ["你是谁？", "你好吗？"],
        config={"max_concurrency": 2}
    )
    for i, response in enumerate(result):
        print(f"响应 {i + 1}: {response.text[:50]}...")


if __name__ == "__main__":
    main()

"""
模型会响应两次，输出内容格式和 invoke 一致
响应 1: 我是通义千问（Qwen），由通义实验室...
响应 2: 我很好，谢谢你的关心...
"""


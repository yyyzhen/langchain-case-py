"""
基础模型配置 - 使用 ChatOpenAI 直接初始化
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 加载环境变量
load_dotenv()

# 使用 ChatOpenAI 直接初始化模型
model = ChatOpenAI(
    model="qwen3-max",
    api_key=os.getenv("MODEL_API_KEY"),
    base_url=os.getenv("MODEL_BASE_URL"),
)


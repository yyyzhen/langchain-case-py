"""
基础模型配置
使用 init_chat_model 或 ChatOpenAI 初始化模型
"""
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# 加载环境变量
load_dotenv()

# 使用 init_chat_model 初始化模型
model = init_chat_model(
  model=os.getenv("MODEL_NAME", "qwen3-max"),
  model_provider='openai',
  base_url=os.getenv("MODEL_BASE_URL"),
  api_key=os.getenv("MODEL_API_KEY"),
  temperature=0.7,
)


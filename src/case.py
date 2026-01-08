"""
主入口文件 - LangChain Python 案例演示
对应 TypeScript 版本的 case.ts

用法:
    python -m src.case
    或者直接运行单个案例:
    python -m src.model_case.invoke_01
"""
import asyncio
import json
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage
from src.base_model import model
from src.utils import print_agent_response


# 创建获取天气工具
@tool
def get_weather(city: str) -> str:
    """获取某地的天气信息"""
    return json.dumps({"city": city, "weather": "晴天"}, ensure_ascii=False)


# 创建获取用户位置工具
@tool
def get_user_location() -> str:
    """获取用户位置"""
    return json.dumps({"location": "海拉鲁大陆"}, ensure_ascii=False)


async def main():
    # 创建 Agent
    agent = create_agent(
        model=model,
        tools=[get_weather, get_user_location],
    )

    # 调用 Agent
    response = await agent.ainvoke({
        "messages": [HumanMessage(content="外面的天气怎么样")]
    })
    
    print_agent_response(response)

if __name__ == "__main__":
    asyncio.run(main())


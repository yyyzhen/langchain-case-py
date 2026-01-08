"""
04 - ToolMessage 示例
ToolMessage 是工具执行结果返回的消息
通常由 Agent 自动创建，我们这里展示完整的工具调用流程
"""
import asyncio
import json
from langchain.agents import create_agent
from langchain.tools import tool
from src.base_model import model
from src.utils import print_agent_response

async def get_weather_api(city: str) -> dict:
    """模拟的天气 API"""
    return {"city": city, "weather": "晴天"}


# 定义工具（使用 async 定义异步工具）
@tool
async def get_weather(city: str) -> str:
    """获取天气信息"""
    result = await get_weather_api(city)
    return json.dumps(result, ensure_ascii=False)


async def main():
    # 创建 Agent
    agent = create_agent(
        model=model,
        tools=[get_weather]  # 只需要传入工具
    )

    # 调用 Agent
    response = await agent.ainvoke({
        "messages": [{"role": "user", "content": "杭州天气怎么样"}]
    })

    # Agent 内部自动完成：
    # 1. AI 决定调用 get_weather
    # 2. Agent 自动执行 get_weather
    # 3. Agent 自动创建 ToolMessage (你不需要手动创建！)
    # 4. Agent 把 ToolMessage 发回给模型
    # 5. 返回最终结果

    print_agent_response(response)

if __name__ == "__main__":
    asyncio.run(main())

"""
输出示例:
===============HumanMessage===================
杭州天气怎么样
===============AIMessage===================
(调用工具 get_weather)
===============ToolMessage===================
{"city":"杭州","weather":"晴天"}
===============AIMessage===================
杭州的天气是晴天。
"""


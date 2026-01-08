"""
05 - ContentBlock 示例
展示消息的 content_blocks 属性，提供对现代 LLM 功能的统一访问
"""
import asyncio
import json
from langchain.agents import create_agent
from langchain.tools import tool
from src.base_model import model


@tool
def get_weather(city: str) -> str:
    """获取天气信息"""
    return json.dumps({"city": city, "weather": "晴天"}, ensure_ascii=False)


async def main():
    # 创建 Agent
    agent = create_agent(
        model=model,
        tools=[get_weather]
    )

    # 调用 Agent
    response = await agent.ainvoke({
        "messages": [{"role": "user", "content": "杭州天气怎么样"}]
    })

    for message in response["messages"]:
        print(f"==============={type(message).__name__}===================")
        # content_blocks 提供了对消息内容的结构化访问
        print("content_blocks:", message.content_blocks if hasattr(message, 'content_blocks') else "N/A")
        print("content:", message.content)


if __name__ == "__main__":
    asyncio.run(main())

"""
输出示例:
===============HumanMessage===================
content_blocks: [{'type': 'text', 'text': '杭州天气怎么样'}]
content: 杭州天气怎么样

===============AIMessage===================
content_blocks: [
  {'type': 'text', 'text': ''},
  {
    'type': 'tool_call',
    'id': 'call_xxx',
    'name': 'get_weather',
    'args': {'city': '杭州'}
  }
]
content: 

===============ToolMessage===================
content_blocks: [{'type': 'text', 'text': '{"city":"杭州","weather":"晴天"}'}]
content: {"city":"杭州","weather":"晴天"}

===============AIMessage===================
content_blocks: [{'type': 'text', 'text': '杭州的天气是晴天。'}]
content: 杭州的天气是晴天。
"""


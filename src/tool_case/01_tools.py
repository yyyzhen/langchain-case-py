"""
01 - Tools 工具定义示例
展示如何定义和使用工具，以及使用 Agent 自动调用工具
"""
import asyncio
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage
from src.base_model import model


# 模拟电影数据库
movie_db = [
    {"title": "喜剧电影1", "year": 2020},
    {"title": "喜剧电影2", "year": 2021},
    {"title": "喜剧电影3", "year": 2021},
    {"title": "戏剧电影1", "year": 2022},
    {"title": "戏剧电影2", "year": 2023},
    {"title": "戏剧电影3", "year": 2023},
    {"title": "动作电影1", "year": 2024},
    {"title": "动作电影2", "year": 2025},
    {"title": "动作电影3", "year": 2025},
]


@tool
def search_database(query: str, limit: int = 5) -> dict:
    """
    搜索数据库电影，返回搜索结果
    
    Args:
        query: 搜索关键词
        limit: 返回结果数量
    """
    results = [movie for movie in movie_db if query in movie["title"]][:limit]
    return {"list": results}


async def main():
    # 创建 Agent
    agent = create_agent(
        model=model,
        tools=[search_database],
        system_prompt="你是一个优秀的数据库搜索员，请根据用户的问题搜索数据库。",
    )

    # 调用 Agent
    response = await agent.ainvoke({
        "messages": [HumanMessage(content="给我找两部戏剧电影，我想看看")]
    })

    for msg in response["messages"]:
        print(f"[{type(msg).__name__}]: {msg.content}")


if __name__ == "__main__":
    asyncio.run(main())


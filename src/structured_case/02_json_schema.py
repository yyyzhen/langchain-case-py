"""
02 - JSON Schema 示例
使用 JSON Schema 定义结构化输出格式
"""
import asyncio
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from src.base_model import model
from langchain.agents.structured_output import ToolStrategy

# 使用 JSON Schema 定义结构化输出
movie_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "description": "电影标题"},
        "year": {"type": "string", "description": "上映年份"},
        "director": {"type": "string", "description": "导演"},
        "genre": {"type": "string", "description": "类型"},
        "plot": {"type": "string", "description": "剧情简介"},
    },
    "required": ["title", "year", "director", "genre", "plot"],
    "additionalProperties": False,
}


async def main():
    # 创建 Agent，设置 JSON Schema 格式，必须使用 ToolStrategy 包装
    agent = create_agent(
        model=model,
        response_format=ToolStrategy(movie_schema),
    )

    # 调用 Agent
    response = await agent.ainvoke({
        "messages": [HumanMessage(content="请推荐一部科幻电影")]
    })

    print("结构化响应:")
    print(response.get("structured_response"))


if __name__ == "__main__":
    asyncio.run(main())

"""
输出示例:
{
  "title": "星际穿越",
  "year": "2014",
  "director": "克里斯托弗·诺兰",
  "genre": "科幻",
  "plot": "在不远的未来，地球环境恶化..."
}
"""


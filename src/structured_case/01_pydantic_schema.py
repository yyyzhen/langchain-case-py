"""
01 - Pydantic Schema 示例
使用 Pydantic 模型定义结构化输出格式
(对应 TS 版本的 zodSchema.ts)
"""
import asyncio
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from src.base_model import model


# 使用 Pydantic 定义结构化输出
class Movie(BaseModel):
    """电影信息结构"""
    title: str = Field(description="电影标题")
    year: str = Field(description="上映年份")
    director: str = Field(description="导演")
    genre: str = Field(description="类型")
    plot: str = Field(description="剧情简介")


async def main():
    # 创建 Agent，设置结构化输出格式
    agent = create_agent(
        model=model,
        response_format=Movie,
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


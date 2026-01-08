"""
04 - 多 Schema 示例
使用多个 Schema，让模型根据上下文选择最合适的输出格式
"""
import asyncio
from pydantic import BaseModel, Field
from typing import Union
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain.messages import HumanMessage
from src.base_model import model


class Movie(BaseModel):
    """电影信息结构"""
    title: str = Field(description="电影标题")
    year: str = Field(description="上映年份")
    director: str = Field(description="导演")
    genre: str = Field(description="类型")
    plot: str = Field(description="剧情简介")


class Book(BaseModel):
    """书籍信息结构"""
    title: str = Field(description="书名")
    author: str = Field(description="作者")
    publisher: str = Field(description="出版社")
    year: str = Field(description="出版年份")
    price: str = Field(description="价格")


async def main():
    # 使用 ToolStrategy 包装多个 schema（使用 Union 类型）
    response_format = ToolStrategy(
        Union[Movie, Book],
        tool_message_content="结构化数据已提取",
    )

    # 创建 Agent
    agent = create_agent(
        model=model,
        response_format=response_format,
    )

    # 调用 Agent - 请求科幻小说
    response = await agent.ainvoke({
        "messages": [HumanMessage(content="请推荐一部科幻小说")]
    })

    print("结构化响应:")
    print(response.get("structured_response"))


if __name__ == "__main__":
    asyncio.run(main())

"""
输出示例 (Book):
{
  title: '三体',
  author: '刘慈欣',
  publisher: '重庆出版社',
  year: '2008',
  price: '23.00'
}
"""


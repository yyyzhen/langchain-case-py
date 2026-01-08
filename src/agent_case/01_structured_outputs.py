"""
01 - Agent 结构化输出示例
展示如何在 Agent 中使用结构化输出
"""
import asyncio
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from src.base_model import model
from src.utils import print_agent_response


class Movie(BaseModel):
    """电影信息结构"""
    title: str = Field(description="电影标题")
    year: str = Field(description="上映年份")
    director: str = Field(description="导演")
    genre: str = Field(description="类型")
    plot: str = Field(description="剧情简介")


async def main():
    # 创建 Agent，设置结构化输出和空工具列表
    agent = create_agent(
        model=model,
        response_format=Movie,
        tools=[]
    )

    # 调用 Agent
    response = await agent.ainvoke({
        "messages": [{"role": "user", "content": "请告诉我周星驰的《功夫》的相关信息"}]
    })

    print_agent_response(response)


if __name__ == "__main__":
    asyncio.run(main())

"""
输出示例:
消息列表:
[HumanMessage]: 请告诉我周星驰的《功夫》的相关信息...
[AIMessage]: (工具调用)...
[ToolMessage]: 结构化数据已提取...

结构化响应:
Movie(
    title='功夫',
    year='2004',
    director='周星驰',
    genre='喜剧/动作',
    plot='...'
)
"""


"""
02 - State 和 Context 示例
展示如何在工具中访问 state 和 context，以及使用 Command 更新状态
"""
import asyncio
from typing import Any, NotRequired
from typing_extensions import TypedDict

from langchain.agents import create_agent, AgentState
from langchain.tools import tool, ToolRuntime
from langchain.messages import HumanMessage, ToolMessage
from langgraph.types import Command
from src.base_model import model


# 定义自定义状态类型
class MyState(AgentState):
    """自定义状态，继承自 AgentState"""
    user_id: NotRequired[str]


# 定义 Context 类型
class MyContext(TypedDict):
    weather: NotRequired[str]


@tool
def get_weather(
    city: str,
    *,
    runtime: ToolRuntime[MyContext, MyState]
) -> Command:
    """
    获取指定城市的天气信息
    
    Args:
        city: 要获取天气的城市名称
    """
    weather_value = runtime.context.get("weather")
    print(f'getWeather: city={city}, user_id={runtime.state.get("user_id")}, weather={weather_value}')
    
    user_id = runtime.state.get("user_id", "unknown")
    if city == "杭州":
        user_id = "hz_user"
    
    weather = runtime.context.get("weather", "大太阳")
    
    return Command(
        update={
            "user_id": user_id,
            "messages": [ToolMessage(
                content=f"城市: {city} 的天气是 {weather}!",
                tool_call_id=runtime.tool_call_id,
            )]
        },
    )


async def main():
    # 创建 Agent，定义状态和上下文 schema
    agent = create_agent(
        model=model,
        tools=[get_weather],
        state_schema=MyState,
        context_schema=MyContext,  # 添加 context_schema
    )

    # 调用 Agent，传入初始状态和上下文
    # 注意：TypedDict 不能直接实例化，需要传递字典
    response = await agent.ainvoke(
        {
            "user_id": "bj_user",
            "messages": [HumanMessage(content="杭州的天气怎么样")],
        },
        context={"weather": "雨天"}  # 使用 context 参数，传递字典
    )

    print("最终状态 user_id:", response.get("user_id"))
    for msg in response["messages"]:
        print(f"[{type(msg).__name__}]: {msg.content}")


if __name__ == "__main__":
    asyncio.run(main())


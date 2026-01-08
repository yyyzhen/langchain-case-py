"""
05 - State 和 Context 示例
展示如何在工具中使用 state 和 context 进行状态管理
"""
import asyncio
from typing import Any, NotRequired
from langchain.agents import create_agent, AgentState
from langchain.tools import tool, ToolRuntime
from langchain.messages import HumanMessage, ToolMessage
from langgraph.types import Command
from langgraph.checkpoint.memory import InMemorySaver
from src.base_model import model


checkpointer = InMemorySaver()


class MyState(AgentState):
    """自定义状态，包含用户画像"""
    profile: NotRequired[dict[str, Any]]


@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    return f"城市: {city} 的天气是晴天!"


@tool
def set_user_profile(
    profile: dict[str, Any],
    *,
    runtime: ToolRuntime[None, MyState]
) -> Command:
    """
    设置用户画像
    
    Args:
        profile: 用户画像信息
    """
    current_profile = runtime.state.get("profile", {})
    return Command(
        update={
            "profile": {**current_profile, **profile},
            # 必须包含 ToolMessage，否则消息历史会变得无效
            "messages": [
                ToolMessage(
                    content=f"用户画像已更新: {profile}",
                    tool_call_id=runtime.tool_call_id
                )
            ],
        }
    )


async def main():
    # 创建 Agent
    agent = create_agent(
        model=model,
        state_schema=MyState,
        tools=[get_weather, set_user_profile],
        system_prompt="""你是一个有用的助手，可以帮用户查询天气，也可以设置用户画像。
每当你调用工具的时候，你都根据之前的上下文内容更新你认为的用户画像。
用户画像的格式为：{key: value}""",
        # checkpointer=checkpointer,  # 可选：启用持久化
    )

    # 第一次调用
    response1 = await agent.ainvoke({
        "profile": {},
        "messages": [HumanMessage(content="杭州明天的天气怎么样，我今天被老师批评了，心情不好，我只是上课说话了，不是故意的")],
    })

    print("response1 profile:", response1.get("profile"))

    # 第二次调用
    response2 = await agent.ainvoke({
        "profile": response1.get("profile", {}),
        "messages": [HumanMessage(content="北京明天的天气怎么样，我和妈妈说了，明天暑假最后一天我要找小明写作业，实际上我明天要找小明打游戏，哈哈")],
    })

    print("response2 profile:", response2.get("profile"))


if __name__ == "__main__":
    asyncio.run(main())


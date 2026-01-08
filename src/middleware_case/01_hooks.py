"""
01 - Middleware Hooks 示例
展示所有可用的中间件钩子
"""
from typing import Any, Callable
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import (
    AgentMiddleware,
    ModelRequest,
    ModelResponse,
    before_agent,
    before_model,
    after_model,
    after_agent,
    wrap_model_call,
    wrap_tool_call,
)
from langchain.tools import tool
from langchain.messages import HumanMessage
from langgraph.runtime import Runtime
from src.base_model import model


@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    return f"城市: {city} 的天气是晴天!"


# 方式1：使用装饰器创建中间件
@before_agent
def log_before_agent(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """Agent 执行前的钩子"""
    print("Agent 执行前")
    return None


@before_model
def log_before_model(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """模型执行前的钩子"""
    print("模型执行前")
    return None


@wrap_tool_call
def log_wrap_tool_call(request: Any, handler: Callable) -> Any:
    """工具调用的包装钩子"""
    print("工具执行前")
    response = handler(request)
    print("工具执行后")
    return response


@wrap_model_call
def log_wrap_model_call(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    """模型调用的包装钩子"""
    print("发送消息给模型前")
    response = handler(request)
    print("收到模型返回的消息后")
    return response


@after_model
def log_after_model(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """模型执行后的钩子"""
    print("模型执行后")
    return None


@after_agent
def log_after_agent(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """Agent 执行后的钩子"""
    print("Agent 执行后")
    return None


# 方式2：使用类创建中间件
class TestMiddleware(AgentMiddleware):
    """测试中间件类"""
    
    def before_agent(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        print("[Class] Agent 执行前")
        return None
    
    def before_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        print("[Class] 模型执行前")
        return None
    
    def wrap_tool_call(self, request: Any, handler: Callable) -> Any:
        print("[Class] 工具执行前")
        response = handler(request)
        print("[Class] 工具执行后")
        return response
    
    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        print("[Class] 发送消息给模型前")
        response = handler(request)
        print("[Class] 收到模型返回的消息后")
        return response
    
    def after_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        print("[Class] 模型执行后")
        return None
    
    def after_agent(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        print("[Class] Agent 执行后")
        return None


def main():
    # 使用装饰器方式的中间件
    agent = create_agent(
        model=model,
        tools=[get_weather],
        middleware=[
            log_before_agent,
            log_before_model,
            log_wrap_tool_call,
            log_wrap_model_call,
            log_after_model,
            log_after_agent,
        ],
    )


    # 也可以使用类方式的中间件
    # agent = create_agent(
    #     model=model,
    #     tools=[get_weather],
    #     middleware=[TestMiddleware()],
    # )

    response = agent.invoke({
        "messages": [HumanMessage(content="你好，我是小明，杭州的天气怎么样")],
    })


if __name__ == "__main__":
    main()

"""
输出顺序示例:
Agent 执行前
模型执行前
发送消息给模型前
收到模型返回的消息后
模型执行后
工具执行前
工具执行后
模型执行前
发送消息给模型前
收到模型返回的消息后
模型执行后
Agent 执行后
"""


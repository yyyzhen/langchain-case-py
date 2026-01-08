"""
公共工具方法
"""
from typing import Any


def print_agent_response(response: dict[str, Any]) -> None:
    """
    格式化打印 Agent 响应
    
    Args:
        response: Agent 的响应字典，包含 messages 和 structured_response
    """
    print("\n" + "*" * 60)
    print("Agent Response")
    print("*" * 60)
    
    # 打印消息列表
    messages = response.get("messages", [])
    for msg in messages:
        msg_type = type(msg).__name__
        
        if msg_type == "HumanMessage":
            print(f"\nHumanMessage: {msg.content}")
            
        elif msg_type == "AIMessage":
            if msg.content:
                print(f"\nAIMessage: {msg.content}")
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    print(f"\nAIMessage [tool_call]: {tc['name']}({tc['args']})")
                    
        elif msg_type == "ToolMessage":
            print(f"\nToolMessage [{msg.name}]: {msg.content}")
            
        else:
            print(f"\n{msg_type}: {msg.content}")
    
    # 打印结构化响应
    structured_response = response.get("structured_response")
    if structured_response:
        print("\n" + "-" * 40)
        print(f"StructuredResponse [{type(structured_response).__name__}]:")
        if hasattr(structured_response, "model_dump"):
            for key, value in structured_response.model_dump().items():
                print(f"  {key}: {value}")
        else:
            print(f"  {structured_response}")
    
    print("\n" + "*" * 60)


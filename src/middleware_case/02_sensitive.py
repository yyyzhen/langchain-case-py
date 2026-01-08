"""数据脱敏中间件 - 保护敏感信息

在模型调用前对消息进行脱敏处理，保护用户隐私。
使用 LangChain 1.x 的 @wrap_model_call 中间件 API。
"""

import re
from typing import List, Dict, Any, Callable
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from langchain.agents import create_agent
from src.base_model import model


# 敏感信息正则表达式模式
SENSITIVE_PATTERNS = {
    "phone": r"1[3-9]\d{9}",  # 中国手机号
    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",  # 邮箱
    "id_card": r"\d{17}[\dXx]",  # 身份证号
    "bank_card": r"\d{16,19}",  # 银行卡号
}

# 预定义的敏感词列表（可根据需要扩展）
SENSITIVE_NAMES: List[str] = ['姚振']  # 敏感姓名列表
SENSITIVE_COMPANIES: List[str] = []  # 敏感公司名列表


def mask_text(text: str, patterns: Dict[str, str] = None) -> str:
    """对文本中的敏感信息进行脱敏处理
    
    Args:
        text: 原始文本
        patterns: 自定义的正则表达式模式字典
    
    Returns:
        脱敏后的文本
    """
    if not text:
        return text
    
    masked_text = text
    use_patterns = patterns or SENSITIVE_PATTERNS
    
    for pattern_name, pattern in use_patterns.items():
        # 根据模式类型生成不同的脱敏标记
        mask_tag = f"[{pattern_name.upper()}_MASKED]"
        masked_text = re.sub(pattern, mask_tag, masked_text)
    
    # 处理敏感姓名
    for name in SENSITIVE_NAMES:
        if name in masked_text:
            masked_text = masked_text.replace(name, "[NAME_MASKED]")
    
    # 处理敏感公司名
    for company in SENSITIVE_COMPANIES:
        if company in masked_text:
            masked_text = masked_text.replace(company, "[COMPANY_MASKED]")
    
    return masked_text


def mask_message(message: BaseMessage) -> BaseMessage:
    """对单条消息进行脱敏处理
    
    Args:
        message: 原始消息
    
    Returns:
        脱敏后的消息
    """
    # 获取消息内容
    content = message.content if isinstance(message.content, str) else str(message.content)
    masked_content = mask_text(content)
    
    # 如果内容没有变化，直接返回原消息
    if masked_content == content:
        return message
    
    # 根据消息类型创建新的脱敏消息
    if isinstance(message, HumanMessage):
        return HumanMessage(content=masked_content)
    elif isinstance(message, AIMessage):
        return AIMessage(content=masked_content)
    elif isinstance(message, SystemMessage):
        return SystemMessage(content=masked_content)
    else:
        # 其他类型消息，尝试复制并修改
        return message.__class__(content=masked_content)


def mask_messages(messages: List[BaseMessage]) -> List[BaseMessage]:
    """对消息列表进行脱敏处理
    
    Args:
        messages: 原始消息列表
    
    Returns:
        脱敏后的消息列表
    """
    return [mask_message(msg) for msg in messages]


@wrap_model_call
def sensitive_data_filter(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """敏感数据过滤中间件
    
    在模型调用前对输入消息进行脱敏处理，保护用户隐私信息。
    
    使用 LangChain 1.x 的 @wrap_model_call 装饰器，
    在模型调用前后进行拦截处理。
    
    Args:
        request: 模型请求对象，包含 messages 等信息
        handler: 下一个处理器（模型调用或下一个中间件）
    
    Returns:
        模型响应对象
    """
    # 对输入消息进行脱敏
    masked_messages = mask_messages(request.messages)
    
    # 使用 override 创建新的请求对象
    new_request = request.override(messages=masked_messages)
    
    # 调用下一个处理器
    return handler(new_request)



def main():
    agent = create_agent(
        model=model,
        system_prompt="你是一个乐于助人的AI助手。",
        middleware=[sensitive_data_filter],
    )
    response = agent.invoke({"messages": [HumanMessage(content="你好，我是姚振，杭州的天气怎么样")]})
    print(response)

if __name__ == "__main__":
    main()
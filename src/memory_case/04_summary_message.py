"""
04 - 消息总结示例
使用 SummarizationMiddleware 自动总结历史消息
"""
import asyncio
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain.messages import HumanMessage, AIMessage
from src.base_model import model
from src.utils import print_agent_response

async def main():
    # 创建使用总结中间件的 Agent
    agent = create_agent(
        model=model,
        middleware=[
            SummarizationMiddleware(
                model=model,  # 用于生成总结的模型
                trigger=("tokens", 50),  # 超过50个token时触发总结
                keep=("messages", 2),  # 保留最近的2条消息
            )
        ],
        system_prompt="你是一个乐于助人的AI助手，能够记住对话历史。",
    )

    # 构造较长的历史消息，触发总结机制
    history = [
        # 第一轮对话 - 关于天气
        HumanMessage(content="你好，我想了解一下北京今天的天气情况"),
        AIMessage(content="你好！北京今天天气晴朗，气温约20-25度，适合外出活动。建议穿着轻薄外套。"),
        # 第二轮对话 - 关于旅游
        HumanMessage(content="那你能推荐一些北京适合春天去的景点吗？"),
        AIMessage(content="当然可以！春天推荐去颐和园赏花，还有植物园的桃花、玉渊潭的樱花都很美。另外故宫和长城也是经典选择。"),
        # 第三轮对话 - 关于美食
        HumanMessage(content="北京有什么特色美食推荐？"),
        AIMessage(content="北京特色美食很多：北京烤鸭（全聚德、便宜坊）、老北京炸酱面、豆汁焦圈、驴打滚、糖葫芦等都值得尝试。"),
        # 第四轮对话 - 关于交通
        HumanMessage(content="从机场到市区怎么走比较方便？"),
        AIMessage(content="从首都机场可以乘坐机场快轨，约25分钟到达东直门。也可以打车或乘坐机场大巴。大兴机场有大兴机场线地铁直达。"),
    ]

    # 调用 Agent，当消息token数超过阈值时，会自动总结旧消息
    response = await agent.ainvoke({
        "messages": [
            *history,
            HumanMessage(content="总结一下我们刚才都聊了什么？"),
        ]
    })

    print_agent_response(response)


if __name__ == "__main__":
    asyncio.run(main())


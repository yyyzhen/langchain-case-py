"""
03 - 数据库工具示例
展示如何创建数据库查询工具，让 Agent 能够执行 SQL 查询
注意：此示例需要安装数据库相关依赖，如 sqlalchemy
"""
import asyncio
from langchain.agents import create_agent
from langchain.tools import tool
from src.base_model import model

# 注意：这是一个示例，实际使用需要配置数据库连接
# from langchain_community.utilities import SQLDatabase
# from sqlalchemy import create_engine


# 模拟数据库查询（实际使用时替换为真实数据库操作）
async def mock_db_run(query: str) -> str:
    """模拟数据库查询"""
    # 在实际应用中，这里会执行真正的 SQL 查询
    return f"执行查询: {query}\n结果: [模拟数据]"


@tool
async def execute_sql(query: str) -> str:
    """
    执行SQL语句，返回结果
    
    Args:
        query: SQL 查询语句
    """
    return await mock_db_run(query)


async def main():
    # 创建 Agent
    agent = create_agent(
        model=model,
        tools=[execute_sql],
        system_prompt="""你是一个谨慎的MySQL数据库分析师。
Rules:
- 一步一步思考。
- 当你需要数据时，使用工具 `execute_sql` 执行一个SELECT查询。
- 只读，不能进行INSERT/UPDATE/DELETE/ALTER/DROP/CREATE/REPLACE/TRUNCATE操作。
- 最多返回5行数据，除非用户明确要求否则不返回更多数据。
- 如果工具返回'Error:', 修改SQL并再次尝试。
- 优先使用明确的列列表，避免使用SELECT *。""",
    )

    # 调用 Agent
    response = await agent.ainvoke({
        "messages": "你好，请告诉我 employees 表中的前5条记录"
    })

    for msg in response["messages"]:
        print(f"[{type(msg).__name__}]: {msg.content}")


if __name__ == "__main__":
    asyncio.run(main())

"""
实际数据库连接示例（需要安装相关依赖）:

from langchain_community.utilities import SQLDatabase

# 连接数据库
db = SQLDatabase.from_uri("mysql+pymysql://root:123456@localhost:3306/employees")

@tool
async def execute_sql(query: str) -> str:
    '''执行SQL语句，返回结果'''
    return db.run(query)
"""


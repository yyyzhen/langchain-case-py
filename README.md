# LangChain Case Python

这是 [langchain-case](../langchain-case) TypeScript 版本的 Python 重写版本，使用 LangChain Python 1.x 版本。

## 安装

```bash
# 使用 uv 安装依赖
uv sync

# 或者使用 pip
pip install -e .
```

## 配置

1. 参考 `.env.example` 中的键值创建 `.env` 文件
2. 填写你的模型 API 配置:

```env
MODEL_API_KEY=your_api_key_here
MODEL_BASE_URL=https://your-api-base-url.com/v1
```

## 运行

```bash
# 运行主案例
python -m src.case

# 运行单个案例
python -m src.model_case.01_invoke
python -m src.model_case.02_stream
python -m src.model_case.03_batch
python -m src.model_case.04_structured_outputs
```

## 目录结构

```
src/
├── base_model.py              # 基础模型配置
├── base_model2.py             # 基础模型配置（使用 ChatOpenAI）
├── utils.py                   # 工具函数
├── case.py                    # 主入口案例文件
├── model_case/                # 模型调用案例
│   ├── 01_invoke.py           # invoke 方法
│   ├── 02_stream.py           # stream 流式调用
│   ├── 03_batch.py            # batch 批量调用
│   └── 04_structured_outputs.py # 结构化输出
├── message_case/              # 消息类型案例
│   ├── 01_system_message.py   # SystemMessage
│   ├── 02_human_message.py    # HumanMessage
│   ├── 03_ai_message.py       # AIMessage
│   ├── 04_tool_message.py     # ToolMessage
│   └── 05_content_block.py    # ContentBlock
├── tool_case/                 # 工具案例
│   ├── 01_tools.py            # 工具定义和使用
│   ├── 02_state_and_context.py # State 和 Context
│   └── 03_db.py               # 数据库工具
├── structured_case/           # 结构化输出案例
│   ├── 01_pydantic_schema.py  # Pydantic Schema
│   ├── 02_json_schema.py      # JSON Schema
│   ├── 03_tool_strategy.py    # ToolStrategy
│   └── 04_multiple.py         # 多 Schema
├── agent_case/                # Agent 案例
│   └── 01_structured_outputs.py # Agent 结构化输出
├── stream_case/               # 流式输出案例
│   ├── 01_messages_mode.py    # messages 模式
│   ├── 02_values_mode.py      # values 模式
│   ├── 03_updates_mode.py     # updates 模式
│   ├── 04_custom_mode.py      # custom 模式
│   ├── 05_multiple_mode.py    # 多模式组合
│   ├── 06_checkpoints_mode.py # checkpoints 模式
│   ├── 07_tasks_mode.py       # tasks 模式
│   └── 08_debug_mode.py       # debug 模式
├── memory_case/               # 记忆案例
│   ├── 01_short_memory.py     # 短期记忆
│   ├── 02_trim_messages.py    # 消息裁剪
│   ├── 03_remove_messages.py  # 消息删除
│   ├── 04_summary_message.py  # 消息总结
│   └── 05_state_and_context.py # State 和 Context
└── middleware_case/           # 中间件案例
    ├── 01_hooks.py            # 中间件钩子
    └── 02_sensitive.py        # 敏感数据过滤中间件示例

```

## 对应关系

| TypeScript 版本 | Python 版本 |
|----------------|-------------|
| `zod` Schema | `Pydantic` BaseModel |
| `createAgent` | `create_agent` |
| `tool()` | `@tool` 装饰器 |
| `HumanMessage` | `HumanMessage` |
| `SystemMessage` | `SystemMessage` |
| `AIMessage` | `AIMessage` |
| `ToolMessage` | `ToolMessage` |
| `createMiddleware` | `AgentMiddleware` 类或装饰器 |
| `MemorySaver` | `InMemorySaver` |

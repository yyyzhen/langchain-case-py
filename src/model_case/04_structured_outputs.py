"""
04 - 结构化输出示例
使用 with_structured_output 方法让模型返回结构化数据
"""
from pydantic import BaseModel, Field
from src.base_model import model


# 定义结构化输出的 Pydantic 模型
class Movie(BaseModel):
    """电影信息"""
    title: str = Field(description="电影标题")
    year: str = Field(description="上映年份")
    director: str = Field(description="导演")
    genre: str = Field(description="类型")
    plot: str = Field(description="剧情简介")


def main():
    # 使用 with_structured_output 绑定结构化输出
    model_with_structure = model.with_structured_output(Movie)
    
    response = model_with_structure.invoke(
        "请告诉我周星驰的《大话西游》的相关信息"
    )
    print(response)


if __name__ == "__main__":
    main()

"""
输出示例（如果模型支持结构化输出）:
Movie(
    title='大话西游',
    year='1995',
    director='刘镇伟',
    genre='喜剧/爱情/奇幻',
    plot='影片讲述了至尊宝为了救回白晶晶...'
)
"""


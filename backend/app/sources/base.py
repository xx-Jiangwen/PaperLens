from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class PaperDTO:
    """统一论文数据传输对象，各数据源适配后的标准结构。
    字段与 Paper ORM 模型对齐，直接用于 upsert。
    """
    id: str                              # 全局唯一 ID，如 "arxiv:1706.03762v7"
    arxiv_id_base: str                   # 去版本号 ID，用于 upsert 去重
    title: str
    authors: list[str]
    abstract: str
    published_at: datetime
    updated_at: Optional[datetime]
    url: str
    pdf_url: Optional[str]
    categories: list[str] = field(default_factory=list)
    primary_category: Optional[str] = None
    comment: Optional[str] = None
    journal_ref: Optional[str] = None
    doi: Optional[str] = None
    source_name: str = "unknown"


class BaseSource(ABC):
    """数据源适配器抽象基类。

    新增数据源（如 Hugging Face Papers、OpenReview）时：
    1. 继承此类，实现 search() 和 fetch_daily()
    2. 在 sources/__init__.py 的 ALL_SOURCES 列表中注册
    3. 定时任务会自动调用所有已注册的源
    """

    @property
    @abstractmethod
    def source_name(self) -> str:
        """数据源唯一名称，如 'arxiv'、'hf_papers'"""
        ...

    @abstractmethod
    async def search(self, query: str, max_results: int = 20) -> list[PaperDTO]:
        """关键词搜索，返回标准化 PaperDTO 列表"""
        ...

    @abstractmethod
    async def fetch_daily(
        self, categories: list[str], max_per_category: int = 50
    ) -> list[PaperDTO]:
        """抓取指定分类的当日最新论文，由定时任务调用"""
        ...

    async def get_by_id(self, paper_id: str) -> Optional[PaperDTO]:
        """根据 ID 获取单篇论文，子类可选择性覆盖"""
        raise NotImplementedError(f"{self.__class__.__name__} 未实现 get_by_id()")

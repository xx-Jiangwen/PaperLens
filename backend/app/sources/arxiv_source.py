import asyncio
from datetime import datetime, timezone
from typing import Optional
import arxiv

from app.sources.base import BaseSource, PaperDTO


class ArxivSource(BaseSource):
    """arXiv 数据源适配器，基于官方 arxiv Python 库。

    复用了原 arxiv_official.py 的核心逻辑，重构为适配器模式。
    原文件保留在 arxiv_crawler_legacy.py 供参考。
    """

    @property
    def source_name(self) -> str:
        return "arxiv"

    async def search(self, query: str, max_results: int = 20) -> list[PaperDTO]:
        """关键词搜索 arXiv 论文"""
        return await asyncio.to_thread(self._search_sync, query, max_results)

    async def fetch_daily(
        self, categories: list[str], max_per_category: int = 50
    ) -> list[PaperDTO]:
        """抓取指定分类的最新论文（按提交日期排序）"""
        results = []
        for cat in categories:
            papers = await asyncio.to_thread(
                self._search_sync,
                f"cat:{cat}",
                max_per_category,
                sort_by=arxiv.SortCriterion.SubmittedDate,
            )
            results.extend(papers)
        # 简单去重（同一篇论文可能属于多个分类）
        seen = set()
        unique = []
        for p in results:
            if p.arxiv_id_base not in seen:
                seen.add(p.arxiv_id_base)
                unique.append(p)
        return unique

    async def get_by_id(self, paper_id: str) -> Optional[PaperDTO]:
        """根据 arXiv ID 获取单篇论文"""
        return await asyncio.to_thread(self._get_by_id_sync, paper_id)

    # ── 同步实现（在线程池中运行）────────────────────────────────

    def _search_sync(
        self,
        query: str,
        max_results: int,
        sort_by: arxiv.SortCriterion = arxiv.SortCriterion.Relevance,
    ) -> list[PaperDTO]:
        client = arxiv.Client()
        search = arxiv.Search(query=query, max_results=max_results, sort_by=sort_by)
        return [self._to_dto(r) for r in client.results(search)]

    def _get_by_id_sync(self, paper_id: str) -> Optional[PaperDTO]:
        clean_id = paper_id.replace("arxiv:", "")
        client = arxiv.Client()
        search = arxiv.Search(id_list=[clean_id])
        results = list(client.results(search))
        return self._to_dto(results[0]) if results else None

    def _to_dto(self, paper: arxiv.Result) -> PaperDTO:
        """arxiv.Result → PaperDTO"""
        raw_id = paper.entry_id.split("/")[-1]           # 如 "1706.03762v7"
        base_id = raw_id.split("v")[0] if "v" in raw_id else raw_id

        return PaperDTO(
            id=f"arxiv:{raw_id}",
            arxiv_id_base=base_id,
            title=paper.title,
            authors=[a.name for a in paper.authors],
            abstract=paper.summary,
            published_at=paper.published.replace(tzinfo=timezone.utc)
                if paper.published.tzinfo is None else paper.published,
            updated_at=paper.updated,
            url=paper.entry_id,
            pdf_url=paper.pdf_url,
            categories=list(paper.categories),
            primary_category=str(paper.primary_category) if paper.primary_category else None,
            comment=paper.comment,
            journal_ref=paper.journal_ref,
            doi=paper.doi,
            source_name=self.source_name,
        )

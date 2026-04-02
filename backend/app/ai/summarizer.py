from typing import AsyncIterator
from app.ai.llm.base import BaseLLM, PaperSummary


class PaperSummarizer:
    """论文摘要生成器。

    同时支持：
    - 流式输出（SSE 接口用，用户实时看到打字机效果）
    - 批量生成（定时任务用，官方额度处理 pending 论文）
    """

    def __init__(self, llm: BaseLLM):
        self._llm = llm

    async def stream(
        self, title: str, abstract: str
    ) -> AsyncIterator[tuple[str, str]]:
        """流式生成，yield (section, delta)"""
        async for section, delta in self._llm.summarize_paper_stream(title, abstract):
            yield section, delta

    async def generate(self, title: str, abstract: str) -> PaperSummary:
        """非流式生成，返回完整摘要"""
        return await self._llm.summarize_paper(title, abstract)

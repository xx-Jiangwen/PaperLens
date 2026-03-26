from app.sources.arxiv_source import ArxivSource
from app.sources.base import BaseSource, PaperDTO

# 所有已注册的数据源，定时任务会遍历此列表
# 新增数据源时，在这里追加即可
ALL_SOURCES: list[BaseSource] = [
    ArxivSource(),
    # HFPapersSource(),   # V2.0
    # OpenReviewSource(), # V2.0
]

__all__ = ["BaseSource", "PaperDTO", "ALL_SOURCES", "ArxivSource"]

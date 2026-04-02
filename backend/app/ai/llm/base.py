from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncIterator, Optional


@dataclass
class LLMConfig:
    """LLM 调用配置，来自用户 BYOK 设置或系统官方额度"""
    base_url: str
    api_key: str
    model_name: str
    temperature: float = 0.3
    max_tokens: int = 256  # 简短摘要，减少 token 上限


@dataclass
class PaperSummary:
    """论文摘要结构化输出"""
    content: str  # 摘要内容（不超过100字）
    model_used: Optional[str] = None


class BaseLLM(ABC):
    """LLM 抽象基类。

    V1.0 只需 OpenAICompatibleLLM 一个实现，即可覆盖：
    OpenAI / DeepSeek / 本地 Ollama（/v1 兼容模式）/ 其他兼容协议模型
    """

    def __init__(self, config: LLMConfig):
        self.config = config

    @abstractmethod
    async def summarize_paper_stream(
        self, title: str, abstract: str
    ) -> AsyncIterator[tuple[str, str]]:
        """流式生成摘要。
        每次 yield: (section_name, delta_text)
        section_name 固定为 'summary'
        """
        ...

    async def summarize_paper(self, title: str, abstract: str) -> PaperSummary:
        """非流式版本，收集流式输出后返回完整摘要"""
        parts: list[str] = []
        async for section, delta in self.summarize_paper_stream(title, abstract):
            parts.append(delta)
        return PaperSummary(
            content="".join(parts),
            model_used=self.config.model_name,
        )

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
    max_tokens: int = 1024


@dataclass
class ThreeSectionSummary:
    """三段式摘要结构化输出"""
    what: str           # 这篇论文做了什么（问题 + 方案）
    how: str            # 用了什么方法（技术路径）
    why: str            # 为什么重要（贡献 + 意义）
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
        """流式生成三段式摘要。
        每次 yield: (section_name, delta_text)
        section_name 取值: 'what' | 'how' | 'why'
        """
        ...

    async def summarize_paper(self, title: str, abstract: str) -> ThreeSectionSummary:
        """非流式版本，收集流式输出后返回完整结构体"""
        sections: dict[str, list[str]] = {"what": [], "how": [], "why": []}
        async for section, delta in self.summarize_paper_stream(title, abstract):
            sections[section].append(delta)
        return ThreeSectionSummary(
            what="".join(sections["what"]),
            how="".join(sections["how"]),
            why="".join(sections["why"]),
            model_used=self.config.model_name,
        )

from typing import AsyncIterator
from openai import AsyncOpenAI

from app.ai.llm.base import BaseLLM, LLMConfig

SUMMARIZE_SYSTEM_PROMPT = """你是一名专业的学术论文分析助手。
请用中文对论文进行简洁摘要，字数不超过100字。

摘要结构：
1. 这篇论文研究什么问题（是什么）
2. 采用了什么方法（怎么样）
3. 取得了什么结果（得到了什么）

直接输出摘要内容，不要加任何标记或标题。"""


class OpenAICompatibleLLM(BaseLLM):
    """兼容 OpenAI 协议的 LLM 实现。

    支持：OpenAI、DeepSeek、本地 Ollama、以及所有 /v1 兼容的模型服务。
    用户只需配置 base_url + api_key + model_name 即可接入。
    """

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self._client = AsyncOpenAI(
            base_url=config.base_url,
            api_key=config.api_key,
            timeout=60.0,  # 60秒超时
        )

    async def summarize_paper_stream(
        self, title: str, abstract: str
    ) -> AsyncIterator[tuple[str, str]]:
        """真正的流式输出，LLM 生成一个 token 就立即返回"""
        user_prompt = f"论文标题：{title}\n\n原始摘要：{abstract}"

        stream = await self._client.chat.completions.create(
            model=self.config.model_name,
            messages=[
                {"role": "system", "content": SUMMARIZE_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            stream=True,
        )

        # 简化为单一摘要，统一用 'summary' 作为 section
        async for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            if delta:
                yield "summary", delta

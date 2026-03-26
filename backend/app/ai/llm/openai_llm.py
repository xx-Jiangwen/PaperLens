from typing import AsyncIterator
from openai import AsyncOpenAI

from app.ai.llm.base import BaseLLM, LLMConfig

SUMMARIZE_SYSTEM_PROMPT = """你是一名专业的学术论文分析助手。
请将论文信息分析为三段式结构化摘要，用中文输出：

输出格式（严格按照此 JSON 格式）：
{
  "what": "【问题与方案】这篇论文解决了什么问题，提出了什么方案...",
  "how": "【技术路径】采用了什么方法、模型或技术...",
  "why": "【贡献与意义】主要创新点和对领域的贡献..."
}

要求：非简单翻译，须提炼核心，每段 2-4 句话。"""


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
        )

    async def summarize_paper_stream(
        self, title: str, abstract: str
    ) -> AsyncIterator[tuple[str, str]]:
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

        # 收集完整响应后解析 JSON 并按段落流式 yield
        # 简化处理：收集完整响应，解析 JSON，然后模拟逐字符流式输出
        full_response = ""
        async for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            full_response += delta

        import json
        try:
            data = json.loads(full_response)
            for section in ("what", "how", "why"):
                text = data.get(section, "")
                # 按词流式 yield（模拟打字机效果）
                for char in text:
                    yield section, char
        except json.JSONDecodeError:
            # 降级：将整个响应放入 what 段
            yield "what", full_response

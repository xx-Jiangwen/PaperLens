from app.ai.llm.base import BaseLLM, LLMConfig
from app.ai.llm.openai_llm import OpenAICompatibleLLM
from app.config import settings


def create_llm(config: LLMConfig) -> BaseLLM:
    """根据配置创建 LLM 实例。
    V1.0 统一使用 OpenAI 兼容层，覆盖主流模型服务。
    """
    return OpenAICompatibleLLM(config)


def create_official_llm() -> BaseLLM:
    """使用系统官方额度创建 LLM（用于批量摘要任务）"""
    config = LLMConfig(
        base_url=settings.OFFICIAL_LLM_BASE_URL,
        api_key=settings.OFFICIAL_LLM_API_KEY,
        model_name=settings.OFFICIAL_LLM_MODEL,
    )
    return create_llm(config)

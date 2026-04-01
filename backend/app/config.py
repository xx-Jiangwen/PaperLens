from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # 数据库
    DATABASE_URL: str = "sqlite+aiosqlite:///./paperpulse.db"

    # 安全
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ENCRYPT_MASTER_KEY: str = "0" * 64  # 32字节 hex，生产必须替换
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天

    # 微信
    WX_APP_ID: str = ""
    WX_APP_SECRET: str = ""
    # 微信订阅消息模板ID（需要在微信公众平台申请）
    WX_SUBSCRIBE_TEMPLATE_ID: str = ""

    # 官方额度 LLM
    OFFICIAL_LLM_BASE_URL: str = "https://api.openai.com/v1"
    OFFICIAL_LLM_API_KEY: str = ""
    OFFICIAL_LLM_MODEL: str = "gpt-4o-mini"

    # 定时任务
    DAILY_CATEGORIES: str = "cs.AI,cs.CL,cs.CV,cs.LG,stat.ML"
    DAILY_MAX_PER_CATEGORY: int = 50

    # 服务
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    @property
    def daily_categories_list(self) -> list[str]:
        return [c.strip() for c in self.DAILY_CATEGORIES.split(",")]


settings = Settings()

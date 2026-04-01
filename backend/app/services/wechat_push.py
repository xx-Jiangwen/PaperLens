"""微信订阅消息推送服务"""
import logging
import httpx
import time
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)


class WeChatPushService:
    """微信小程序订阅消息推送"""

    BASE_URL = "https://api.weixin.qq.com"

    def __init__(self):
        self.app_id = settings.WX_APP_ID
        self.app_secret = settings.WX_APP_SECRET
        self._access_token: Optional[str] = None
        self._token_expires_at: Optional[int] = None

    async def get_access_token(self) -> str:
        """获取小程序 access_token"""
        if self._access_token and self._token_expires_at:
            # 提前 5 分钟刷新
            if time.time() < self._token_expires_at - 300:
                return self._access_token

        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.BASE_URL}/cgi-bin/token",
                params={
                    "grant_type": "client_credential",
                    "appid": self.app_id,
                    "secret": self.app_secret,
                },
            )
            data = resp.json()

        if "errcode" in data:
            logger.error(f"获取 access_token 失败: {data}")
            raise Exception(f"微信 API 错误: {data.get('errmsg')}")

        self._access_token = data["access_token"]
        self._token_expires_at = data["expires_in"] + int(time.time())
        logger.info("access_token 已更新")
        return self._access_token

    async def send_subscribe_message(
        self,
        openid: str,
        template_id: str,
        data: dict,
        page: str = "pages/home/index",
    ) -> bool:
        """发送订阅消息

        Args:
            openid: 用户 openid
            template_id: 消息模板 ID
            data: 模板数据，如 {"thing1": {"value": "今日论文"}}
            page: 用户点击后跳转的小程序页面

        Returns:
            是否发送成功
        """
        try:
            token = await self.get_access_token()

            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{self.BASE_URL}/cgi-bin/message/subscribe/send",
                    params={"access_token": token},
                    json={
                        "touser": openid,
                        "template_id": template_id,
                        "page": page,
                        "data": data,
                        # miniprogram_state: "developer" | "trial" | "formal"
                        "miniprogram_state": "formal",
                    },
                )
                result = resp.json()

            if result.get("errcode") == 0:
                logger.info(f"订阅消息发送成功: {openid}")
                return True
            else:
                logger.error(f"订阅消息发送失败: {result}")
                return False

        except Exception as e:
            logger.error(f"发送订阅消息异常: {e}")
            return False


# 全局实例
push_service = WeChatPushService()
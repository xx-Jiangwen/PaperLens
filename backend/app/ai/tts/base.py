from abc import ABC, abstractmethod


class BaseTTS(ABC):
    """TTS 抽象基类（留口子）。

    V1.0：微信小程序端直接调用微信内置 TTS，后端不介入。
    V2.0：实现 VolcengineTTS / ElevenLabsTTS 等，后端生成音频文件并返回 URL。
    """

    @abstractmethod
    async def synthesize(self, text: str, voice: str = "default") -> bytes:
        """将文本转为音频字节流（MP3/WAV）"""
        ...

    @abstractmethod
    async def list_voices(self) -> list[dict]:
        """列出可用音色"""
        ...

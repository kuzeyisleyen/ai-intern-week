from typing import Protocol, Any

class ChatModel(Protocol):
    """
    Sistemin dil modelleriyle iletişim kurması için gereken minimum sözleşme.
    Uygulama katmanı HTTP detaylarını veya Ollama spesifikasyonlarını bilmemelidir.
    """
    def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        response_format: dict | None = None,
        options: dict | None = None,
        think: bool | None = None,
    ) -> dict:
        ...
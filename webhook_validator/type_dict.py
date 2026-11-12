from typing import TypedDict


class WebhookRequestTypeDict(TypedDict):
    headers: dict[str, str]
    body: dict[str, object]
    
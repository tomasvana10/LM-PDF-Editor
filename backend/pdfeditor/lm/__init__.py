from typing import cast, final
import requests
from urllib import parse

from ..data import read_data


@final
class LMClient:
    _pre_prompt: str = read_data("preprompt.txt")

    host: str
    port: int
    url: str

    def __init__(self, *, host: str = "localhost", port: int = 1234):
        self.host = host
        self.port = port

        self.url = f"http://{self.host}:{self.port}/api/v0/"

    def _ask(self, prompt: str, model: str) -> str:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.8,
            "max_tokens": 1000000,
        }

        resp = requests.post(
            parse.urljoin(self.url, "chat/completions"), json=payload, timeout=1200
        )
        resp.raise_for_status()
        data = resp.json()

        return data["choices"][0]["message"]["content"]

    def ask_plain(self, prompt: str, model: str) -> str:
        return self._ask(prompt, model)

    def ask_full(self, user_context: str, original_html: str, model: str) -> str:
        prompt = (
            self.__class__._pre_prompt
            + "\n\n"
            + f"User context:\n{user_context}\n\n"
            + f"Original HTML:\n{original_html}"
        )

        return self._ask(prompt, model)

    def get_models(self, *, only_active: bool = False):
        resp = requests.get(parse.urljoin(self.url, "models"))
        resp.raise_for_status()

        data = resp.json()["data"]

        return cast(
            list[dict[str, str | int | list[str]]],
            [model for model in data if not only_active or model["state"] == "loaded"],
        )


__all__ = ["LMClient"]

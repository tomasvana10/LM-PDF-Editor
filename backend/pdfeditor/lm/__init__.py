from typing import cast, final
import requests
from urllib import parse

from ..data import read_data
from ..settings import get_settings


@final
class LMClient:
    _pre_prompt: str = read_data("preprompt.txt")

    host: str
    port: int
    url: str

    def __init__(self):
        settings = get_settings()
        self.host = settings["lms_host"]
        self.port = settings["lms_port"]

        self.url = f"http://{self.host}:{self.port}/api/v0/"

    def _ask(self, prompt: str, model: str) -> str:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.8,
            "max_tokens": -1,
            "stream": False,
        }

        resp = requests.post(
            parse.urljoin(self.url, "chat/completions"), json=payload, timeout=1200
        )
        resp.raise_for_status()
        data = resp.json()

        return data["choices"][0]["message"]["content"]

    def process_html(self, user_context: str, original_html: str, model: str) -> str:
        prompt = (
            self.__class__._pre_prompt
            + "\n\n"
            + f"User instruction:\n{user_context}\n\n"
            + f"Original HTML you must edit (if there is none, you are not editing, but creating):\n{original_html}"
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

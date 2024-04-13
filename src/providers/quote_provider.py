from abc import ABC, abstractmethod

import httpx
from bs4 import BeautifulSoup


class QuoteProvider(ABC):
    @abstractmethod
    def get_random_quote(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_quotes(self, *args, **kwargs):
        pass

    @staticmethod
    def load_data(url: str, max_retries: int = 3):
        retry_count = 0
        while retry_count < max_retries:
            try:
                with httpx.Client() as client:
                    response = client.get(url)
                    if response.status_code == 200:
                        return BeautifulSoup(response.text, "html.parser")
            except httpx.RequestError as httpx_error:
                print(
                    f"Failed to connect with remote server. Retrying ({retry_count + 1}/{max_retries})...\n Here our preferred quote: "
                )
            finally:
                client.close()
            retry_count += 1
        print(
            "Failed to retrieve quotes after several attempts. Please try again later !"
        )

    @staticmethod
    def reformat_quote(quote: str) -> str:
        return quote.replace("“", "").replace("”", "")
